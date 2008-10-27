#!/usr/bin/env python
#coding=utf-8


from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext as _T

class Keyword(models.Model):
    """This represent keywords of papers""" 
    word = models.CharField(max_length=200, db_index=True)          # 关键词
    def __unicode__(self):
        return self.word
admin.site.register(Keyword)

class TextVersion(models.Model):
    """This represent a version of a text. Each edition will create a new version"""
    icon = models.IntegerField(default=0)                           # 表情符号
    title = models.CharField(max_length=200, blank=False)           # 文件名
    content = models.TextField(blank=True)                          # 文件的内容（HTML格式）
    birth = models.DateTimeField(auto_now_add=True)                 # 上传日期
    owner = models.ForeignKey(User)                                 # 上传的人
    postIP = models.IPAddressField(blank=False)                     # 发帖的IP地址
    previous = models.ForeignKey('self', null=True, blank=True, default="NULL") # 前一个版本，NULL表示是第一个版本
    def __unicode__(self):
        return self.title
admin.site.register(TextVersion)
    
class Article(models.Model):
    """一篇文章"""
    topVersion = models.ForeignKey(TextVersion)                     # 当前的文章 
    birth = models.DateTimeField(auto_now_add=True)                 # 第一次发表的日期
    privileges = models.CharField(max_length = 200, blank=True, default="") # 访问权限
    keywords = models.ManyToManyField(Keyword, blank=True)                      # 关键词
    parent = models.ForeignKey('self', null=True, related_name="parent_article", default="NULL", blank=True) # 回复哪一篇文章，非回复的文章是NULL
    root = models.ForeignKey('self', null=True, related_name="root_article", default="NULL", blank=True)     # 回复的第一篇文章。非回复的文章是NULL
    lat = models.DateTimeField()                                    # 最后一次回复的日期
    def __unicode__(self):
        return unicode(self.topVersion)
    
admin.site.register(Article)

class Folder(models.Model):
    """一组文章的集合，或者一组上传文件的分类。比如一个人blog的文章，一个BBS的板块等等"""
    name = models.CharField(max_length=200, db_index=True)           # 名称
    root = models.ForeignKey('self', null=True, blank=True, default="NULL", related_name="root_group")
    parent = models.ForeignKey('self', null=True, blank=True, default="NULL", related_name="parent_group")
    children = models.ManyToManyField('self', blank=True, related_name="children")
    articles = models.ManyToManyField(Article, blank=True)
    privileges = models.CharField(max_length = 200, blank=True, default="") # 访问权限
    owner = models.ForeignKey(User)                                 # 所有人
    birth = models.DateTimeField(auto_now_add=True)                 # 创建日期
    lat = models.DateTimeField()                                    # 最后一次回复的日期
    note = models.TextField(blank=True, default="")                                 # 其它说明
    def __unicode__(self):
        return unicode(self.name)
admin.site.register(Folder)

class Forum(Folder):
    """论坛"""
    masters = models.ManyToManyField(User, related_name="tops", blank=True)         # 版主
    toparticle = models.ManyToManyField(Article, related_name="tops", blank=True)   # 置顶文章
    forbidden = models.ManyToManyField(User, related_name="forbid", blank=True)     # 封禁人员
admin.site.register(Forum)    
