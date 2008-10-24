#!/usr/bin/env python
#coding=utf-8


from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext as _T


# Create your models here.

class ConfigTree(models.Model):
    """用于保存网站配置的树形注册表"""
    parent = models.ForeignKey('self', null=True, default=None, blank=True) # 父节点，为None说明是根节点
    key = models.CharField(max_length=100, db_index=True)   # 键名
    content = models.TextField(blank=True, default="")      # 内容，建议保存pickle序列化的串
    
