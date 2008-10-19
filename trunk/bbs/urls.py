#!/usr/bin/env python
#coding=utf-8


from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^/', 'index'),
    (r'^admin/(.*)', admin.site.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
     
    (r'^accounts/', include('accounts.urls')),
    (r'^uploads/', include('uploads.urls')),
    # (r'^addresses/(.*)', include('addresses.urls')),
    # (r'^news/(.*)', include('accounts.newsurls')),
    # (r'^forum/(.*)', include('articles.bbsurls')),
    # (r'^bbs/(.*)', include('articles.bbsurls')),
    # (r'^blog/(.*)', include('articles.blogurls')),
    # (r'^wiki/(.*)', include('articles.wikiurls')),
)
