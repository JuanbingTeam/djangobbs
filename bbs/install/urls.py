#!/usr/bin/env python
#coding=utf-8


from django.conf.urls.defaults import *

urlpatterns = patterns('install.views',
    (r'^$', 'index'),               # "用户主页"
)
