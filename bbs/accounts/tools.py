#!/usr/bin/env python
#coding=utf-8



from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.contrib import auth

def findUser(nickName):
    try:
        return UserProfile.objects.get(nickName = nickName)
    except UserProfile.DoesNotExist:
        pass
    
    try:
        user = User.objects.get(email = nickName)
        if user != None:
            return UserProfile.objects.get(user = user)
    except User.DoesNotExist:
        pass
    except User.MultipleObjectsReturned:
        pass
    except UserProfile.DoesNotExist:
        print "shit"
        pass

    return None

def authenticate(username, password):
    user = findUser(username)
    if user:
        return auth.authenticate(username=user.user.username, password=password)
    else:
        return user

def login(request, user):
    user.lastLoginIP = request.META['REMOTE_ADDR']
    user.save()
    request.profile = user
    return auth.login(request, user.user)


def logout(request):
    return auth.logout(request)
