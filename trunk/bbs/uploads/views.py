#!/usr/bin/env python
#coding=utf-8

# Create your views here.

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from uploads.models import *

from cStringIO import StringIO

import Image, ImageDraw # 需要PIL支持 

@login_required
def upload(request):
    data = {'request':request, 'user':user}
    if len(HttpRequest.FILES) == 0:
        return render_to_response('uploads/upload.html', data)
    else:
        result = []
        for i in request.FILES:
            result.append(saveFile(request.user, i))
        data['files'] = result
        return render_to_response('uploads/upload_report.html', data)

def list_by_user(request, id):
    try:
        user = User.objects.get(id=id)
        files = UploadResource.objects.filter(owner=user);
        data = {'user':User.objects.get(id=id), 'request':request}

        if files.count() == 0:
            return render_to_response('uploads/nouploads.html', data)
        else:
            if request.REQUEST.has_key('page'):
                start_page = int(request.REQUEST['page'])
            else:
                start_page = 1
            
            if  request.REQUEST.has_key('pagesize'):
                page_size = int(request.REQUEST['page_size'])
            else:
                page_size = 50
    
            pages = Paginator(files, page_size)
            data['pages'] = pages
            data['content'] = pages.page(start_page)
            return render_to_response('uploads/list.html', data)
    except:
        return HttpResponseNotFound()  
    

def get_gif_thumbnail(request, id, x, y):
    # TODO
    pass

def get_png_thumbnail(request, id, x, y):
    # TODO
    pass

def get_jpg_thumbnail(request, id, x, y):
    # TODO
    pass

def get_photo(request, id, x, y):
    # TODO
    pass
