#!/usr/bin/env python
#coding=utf-8



from djangobbs.accounts.models import *
from django.contrib.auth.models import User
from django.contrib import auth

def finduser(nickName):
    """该函数根据用户的nickname或者email来查找用户。找到的话返回该用户的profile，否则返回None"""
    try:
        return UserProfile.objects.get(nickname_iexact = nickName)
    except UserProfile.DoesNotExist:
        pass
    
    try:
        return User.objects.get(email = nickName).get_profile()
    except User.DoesNotExist:
        pass
    except User.MultipleObjectsReturned:
        pass
    except UserProfile.DoesNotExist:
        pass

    return None

def authenticate(username, password):
    user = finduser(username)
    if user:
        return auth.authenticate(username=user.user.username, password=password)
    else:
        return user

def login(request, user):
    if isinstance(user, User):
        return login(request, user.get_profile())
    else:
        assert isinstance(user, UserProfile)
        result = auth.login(request, user.user) 
        objs = ExtraProfileEntry.objects.filter(time='I')
        for i in objs:
            data = i.get_request_data(request)
            i.push(user, data)
        return result

def logout(request):
    user = request.user
    if user.is_anonymous():
        pass
    else:
        profile = user.get_profile()
        objs = ExtraProfileEntry.objects.filter(time='O')
        for i in objs:
            data = i.get_request_data(request)
            i.push(user, data)
    
    return auth.logout(request)
