#!/usr/bin/env python
#coding=utf-8


from django.conf.urls.defaults import *
from django.contrib import admin
from index import index

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', index),
    (r'^admin/(.*)', admin.site.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
     
    (r'^accounts/', include('djangobbs.accounts.urls')),
    (r'^uploads/', include('djangobbs.uploads.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': r'../templates/media'}),                       
)
