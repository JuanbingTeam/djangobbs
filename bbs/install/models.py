#!/usr/bin/env python
#coding=utf-8


from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext as _T
from cPickle import loads, dumps


# Create your models here.

class ConfigTree(models.Model):
    """用于保存网站配置的树形注册表"""
    parent = models.ForeignKey('self', null=True, default=None, blank=True) # 父节点，为None说明是根节点
    key = models.CharField(max_length=100, db_index=True)   # 键名
    content = models.TextField(blank=True, default="")      # 内容，建议保存pickle序列化的串
    
    @static_method
    def get_config(path, default=None):
        path = path.split("/")
        record = None
        try:
            for i in path:
                record = ConfigTree.objects.get(parent=record, key=i)
            return loads(record.content)      
        except ConfigTree.DoesNotExist:
            return default
        
    @static_method
    def put_config(path, data):
        path = path.split("/")
        record = None
        try:
            for i in path[:-1]:
                record = ConfigTree.objects.get(parent=record, key=i)
            try: 
                record = ConfigTree.objects.get(parent=record, key=i)
            except ConfigTree.DoesNotExist:
                result = ConfigTree()
                result.parent = record
                result.key = path[-1]
                record = result
            record.content = dumps(data)
            record.save()      
        except ConfigTree.DoesNotExist:
            return default    

