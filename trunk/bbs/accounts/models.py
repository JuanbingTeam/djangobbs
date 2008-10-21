#!/usr/bin/env python
#coding=utf-8


from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext as _T

from addresses.models import Person
from accounts.config import LOGO_FOLDER


class ExtraUserProfile(models.Model):
    """该表记录了针对每个用户需要额外记录的字段"""
    EXTERNAL_ENTRY_COLLECT_SOURCE = (
        ('X', _T("由用户填写")),
        ('？', _T("未定义，由app自行决定")),
        ('M', _T("从request.META读出")),
        ('G', _T("从request.GET读出")),
        ('P', _T("从request.POST读出")),
        ('R', _T("从request.REQUEST读出")),
        ('C', _T("从request.COOKIES读出")),
        ('T', _T("记录当前的时间")),
    )
    
    """该表记录了针对每个用户需要额外记录的字段"""
    EXTERNAL_ENTRY_COLLECT_TIME = (
        ('R', _T("注册时要求填写")),
        ('I', _T("登陆时自动记录")),
        ('O', _T("登出时自动记录")),
        ('A', _T("每次请求都记录")),
        ('?', _T("预留，由各个应用自行决定")),
    )

    name = models.CharField(max_length=100, unique=True, db_index=True)
    source =models.CharField(max_length=1, default='X', choices=EXTERNAL_ENTRY_COLLECT_SOURCE)
    time =models.CharField(max_length=1, default='R', choices=EXTERNAL_ENTRY_COLLECT_TIME)
    type = models.CharField(max_length=1, default='R', choices=EXTERNAL_ENTRY_COLLECT_TIME)
    duplication = models.PositiveIntegerField()
    key_word = models.TextField(blank=True, default="")
    
    def __unicode__(self):
        return self.name
        
admin.site.register(ExtraUserProfile)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    # 用户名，由于User本身的用户名不允许使用中文，所以改用该名作为用户的真正登陆名称
    nick_name = models.CharField(max_length=60, unique=True, db_index=True, blank=False)
    logo = models.FilePathField(path=LOGO_FOLDER, recursive=True, blank=True, db_index=True)
    personal_data = models.ForeignKey(Person, null=True, db_index=True, blank=False)
    extra_data=models.ManyToManyField(ExtraUserProfile, through='ExtraUserData')

    def __unicode__(self):
        return self.nickName
admin.site.register(UserProfile)

class ExtraUserData(models.Model):
    """此表用来保存附加的用户信息"""
    user = models.ForeignKey(UserProfile)
    extra_data = models.ForeignKey(ExtraUserProfile)
    content = models.TextField(blank=True, default="")
admin.site.register(UserProfile)    

