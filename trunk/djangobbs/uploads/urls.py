#!/usr/bin/env python
#coding=utf-8

"""处理用户上传和下载资源"""

from django.conf.urls.defaults import *
urlpatterns = patterns('djangobbs.uploads.views',
    (r'^upload/$', 'upload'),                    # 上传文件
    (r'^list/(?P<id>\d+)/$', 'list_by_user'),     # 列出用户上传的所有文件
    
    (r'^thumb/gif/(?P<id>\d+)/(?P<x>\d+).(?P<y>\d+)/$', 'get_gif_thumbnail'),    # 返回GIF格式的缩略图
    (r'^thumb/png/(?P<id>\d+)/(?P<x>\d+).(?P<y>\d+)/$', 'get_png_thumbnail'),    # 返回PNG格式的缩略图
    (r'^thumb/jpg/(?P<id>\d+)/(?P<x>\d+).(?P<y>\d+)/$', 'get_jpg_thumbnail'),    # 返回JPG格式的缩略图
    
    (r'^download/(?P<id>\d+)/$', 'download_file'),    # 以附件的形式下载文件
    (r'^file/(?P<id>\d+)/$', 'get_file'), # 直接获得文件
    
    (r'^photo/(?P<id>\d+)/$', 'get_photo'),      # 返回带日戳的照片
)
