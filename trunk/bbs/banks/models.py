#coding=utf-8
#!/usr/bin/env python


from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext as _T

class Bank(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True, blank=False)
    author = models.ForeignKey(User);
    birthday = models.DateTimeField(auto_now_add=True);
    