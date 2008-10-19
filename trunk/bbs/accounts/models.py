#!/usr/bin/env python
#coding=utf-8


from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext as _T

from addresses.models import Person
from articles.models import Article
from uploads.models import UploadResource


class UserProfile(Person):
    user = models.ForeignKey(User, unique=True)
    nickName = models.CharField(max_length=200, unique=True, db_index=True, blank=False)
    logo = models.ForeignKey(UploadResource, null=True, blank=True, default="NULL")
    lastLoginIP = models.IPAddressField(blank=True, default="")
    plan = models.ForeignKey(Article, null=True, blank=True, default="NULL")
    friends = models.ManyToManyField(User, blank=True, related_name="friends");
    enemies = models.ManyToManyField(User, blank=True, related_name="enemies");
    def __unicode__(self):
        return self.nickName
admin.site.register(UserProfile)
