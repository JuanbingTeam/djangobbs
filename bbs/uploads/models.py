#!/usr/bin/env python
#coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext as _T 
from uploads.config import UPLOAD_FILE_FOLDER

class MimeType(models.Model):
    """文件类型"""
    extname = models.CharField(max_length=10, db_index=True, unique=True) # "扩展名"
    major = models.CharField(max_length=20, default="application")    
    minor = models.CharField(max_length=20)
    magic_number = models.CharField(max_length=20, blank=True, default="") # 魔数，指文件开头的几个固定不变的字节，用于验证上传文件的真实性。 

    def __unicode__(self):
        return self.major + u"/" + self.minor
admin.site.register(MimeType)

class UploadResource(models.Model):
    """用户上传的文件"""
    filename = models.FileField(upload_to=UPLOAD_FILE_FOLDER, max_length=200, db_index=True)   # 文件名称
    mime = models.ForeignKey(MimeType)                                                  # 类型
    md5code = models.CharField(max_length = 32, blank=True, default="", db_index=True)  # MD5号，用于筛查重复的文件
    birth = models.DateTimeField(auto_now_add=True, db_index=True)                      # 上传日期
    owner = models.ForeignKey(User)                                                     # 上传的人
    taketime = models.DateTimeField(null=True, blank=True, db_index=True)   # 如果用户上传的是照片，记录其拍摄日期
    def __unicode__(self):
        return self.filename
admin.site.register(UploadResource)
