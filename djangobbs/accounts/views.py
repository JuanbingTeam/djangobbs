#!/usr/bin/env python
#coding=utf-8


from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.core.mail import send_mail
from cStringIO import StringIO

import Image, ImageDraw
from djangobbs.accounts.models import *
from djangobbs.accounts.forms import *
from djangobbs.accounts.config import *
from djangobbs.accounts import tools

def index(request, id):
    data = {'user' : request.user }
    try:
        data['profile'] = request.user.get_profile()
    except UserProfile.DoesNotExist:
        pass 

    return render_to_response('accounts/user.html', data) 
    
def login(request, template = 'accounts/login.html'):
    if request.session.has_key('validation') and request.method == 'POST':
        form = LoginForm(request.POST)
        form.code = request.session['validation']
        request.session['validation'] = ""
        form.hasCookie = request.session.test_cookie_worked()
        if form.is_valid():
            form.cleaned_data['user'].user = tools.authenticate(username=form.cleaned_data['user'].user.username, password=form.cleaned_data['password'])
            tools.login(request, form.cleaned_data['user'])
            if not form.cleaned_data['saveLogin']:
                request.session.set_expiry(0)
            if request.REQUEST.has_key('next'):
                next = request.REQUEST['next']
            else:
                next = '/'
            return HttpResponseRedirect(next)
    else:
        form = LoginForm()
    request.session.set_test_cookie()
    return render_to_response(template, {'form': form})

def logout(request, template = 'accounts/logout.html'):
    tools.logout(request)
    return render_to_response(template, request)

def register(request, autoActive=True):
    if not request.POST.has_key('accept_eula'):
        return render_to_response('accounts/eula.html', {'request':request})

    form = RegisterForm(request.POST)
    form.code = request.session['validation']
    request.session['validation'] = ""
    form.hasCookie = request.session.test_cookie_worked()
    if form.is_valid():
        return HttpResponseRedirect(next)
    else:
        form = RegisterForm()
    request.session.set_test_cookie()
    return render_to_response('', {'form': form} )

@login_required
def password(request):
    pass

def resetPassword(request):
    pass

def validate(request, length = 5):
    password = User.objects.make_random_password(length, allowed_chars='ABCDEFGHJKLMNPQRUSTUVWXY')
    request.session['validation'] = password
    img = VALIDATE_IMAGE_BACK_GROUND.copy()
    draw = ImageDraw.Draw(img)
    size = draw.textsize(password, font = VALIDATE_IMAGE_FONT)
    draw.text((0, 0), password, fill=VALIDATE_IMAGE_FORE_GROUND, font = VALIDATE_IMAGE_FONT)
    img = img.crop((0, 0, size[0], size[1]))
    buf = StringIO()
    img.save(buf, "jpeg")
    result = HttpResponse(mimetype='Image/jpeg')
    result.write(buf.getvalue())
    buf.close()
    return result

