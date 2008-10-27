#!/usr/bin/env python
#coding=utf-8


from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext as _T

from addresses.models import Person
from accounts.config import LOGO_FOLDER
from cPickle import dumps

class UserProfile(models.Model):
    # 默认关联django.contrib.auth.models.User. 这是UserProfile的标准用法
    user = models.ForeignKey(User, unique=True)

    # 用户名，由于User本身的用户名不允许使用中文，所以改用该名作为用户的真正登陆名称
    nickname = models.CharField(max_length=200, unique=True, db_index=True, blank=False)
    
    # 用户的头像。保存在LOGO_FOLDER目录下
    logo = models.FileField(upload_to=LOGO_FOLDER, blank=True, default="")
    
    # 用户的私人信息，用户可以可以不填。
    personal_data = models.ForeignKey(Person, null=True, db_index=True, blank=True, default="")
    
    # 用户的附加
    extradata = models.ManyToManyField('accounts.ExtraProfileEntry', through='ExtraUserData')

    def __unicode__(self):
        return self.nickname

admin.site.register(UserProfile)

class ExtraUserData(models.Model):
    """此表真正保存用户的附加数据"""
    
    # 对应该项的用户
    user = models.ForeignKey(UserProfile)
    
    # 对应的项
    entry = models.ForeignKey('accounts.ExtraProfileEntry')
    
    # 记录的内容
    content = models.TextField(blank=True, default="")
    
    # 记录的时间
    time = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return unicode(self.user) + u'.' + unicode(self.entry) + u'@' + unicode(self.time) + u'.' + self.content

admin.site.register(ExtraUserData)    

EXTERNAL_ENTRY_COLLECT_SOURCE = (
    ('U', _T('By User')),        # 由用户填写
    ('?', _T('Undefined')),      # 系统保留。由各个应用自行决定用法
    ('M', _T('request.META')),   # 从request.META读出
    ('G', _T('request.GET')),    # 从request.GET读出
    ('P', _T('request.POST')),   # 从request.POST读出
    ('R', _T('request.REQUEST')),# 从request.REQUEST读出
    ('C', _T('request.COOKIE')), # 从request.COOKIES读出
    ('s', _T('request.session')),# 从request.session读出
    ('F', _T('request.FILES')),  # 从request.FILES读出
)

EXTERNAL_ENTRY_COLLECT_TIME = (
    ('R', _T('At register')),    # 注册时要求填写, 注册后用户不可更改
    ('M', _T('Manual')),         # 注册时填写, 注册后可以由用户手动更改
    ('I', _T('At login')),       # 登陆时自动记录,
    ('O', _T('At logout')),      # 登出时自动记录,
    ('A', _T('At all request')), # 每次请求都记录,
    ('?', _T('Undefined')),      # 系统保留。由各个应用自行决定用法
)

class ExtraProfileEntry(models.Model):
    """This model records all extra user information required by the bbs system."""
    
    # 给该项取的一个名称。比如'login IP', 'access time'
    name = models.CharField(max_length=100, unique=True, db_index=True)
    
    # 取得数据的方式，可以从request里自动获取，或者由用户提供。默认由用户手动提供。参考EXTERNAL_ENTRY_COLLECT_TIME的注释
    source = models.CharField(max_length=1, default='U', choices=EXTERNAL_ENTRY_COLLECT_SOURCE)
    
    # 取得数据的时机。是每次登录记录，还是每次请求都记录，还是别的什么，参考EXTERNAL_ENTRY_COLLECT_TIME的注释
    time = models.CharField(max_length=1, default='M', choices=EXTERNAL_ENTRY_COLLECT_TIME)
    
    # 用于验证数据，具体还没想好怎么个用法。可能是正则表达式？或者别的什么。
    type = models.TextField(blank=True, default='') 
    
    # 允许重复出现的次数，默认每个用户每个项目只记录一次。
    dupli = models.PositiveIntegerField(null=True, default=1)
    
    # 自动从request字典里读取时对应的关键字，如果是*则将整个字典的内容都记录下来（使用pickle序列化后保存）
    keyword = models.TextField(blank=True, default="")
    
    def __unicode__(self):
        return self.name
    
    def push(self, user, data):
        """保存额外的用户数据"""
        record = ExtraUserData()
        record.user = user
        record.entry = self
        record.content = data
        record.save()
        
        if self.dupli != None:
            objs = ExtraUserData.objects.filter(user=user).filter(entry=self)
            if objs.count() > self.dupli:
                obj = objs.order_by('time')[0] # order by time. the 1st is the oldest record.
                obj.delete()

    def get_request_data(self, request):
        """该函数从request里取出需要保存的数据"""
        dict = None
        if self.source == 'M':
            dict = request.META
        elif self.source == 'G':
            dict = request.GET
        elif self.source == 'P':
            dict = request.POST
        elif self.source == 'R':
            dict = request.REQUEST
        elif self.source == 'C':
            dict = request.COOKIE
        elif self.source == 's':
            dict = request.session
        elif self.source == 'F':
            dict = request.FILES
        else:
            dict = None
            
        if dict != None:
            if self.keyword == '*':
                return dumps(dict)
            elif dict.has_key(self.keyword):
                return dict.get(self.keyword)
        return ""
                
admin.site.register(ExtraProfileEntry)


"""以下是初始化数据内容的"""
try:
    superuser = User.objects.get(id=1)
    UserProfile.objects.get(user=superuser)
except UserProfile.DoesNotExist:
    """以下代码试图为第一个超级用户初始化一个UserProfile"""
    profile = UserProfile()
    profile.user = superuser
    profile.nickname = superuser.username
    profile.personal_data = None
    profile.save()
except Exception, error:
    pass


try:    
    if ExtraProfileEntry.objects.all().count() == 0:
        """以下代码使得系统默认记录用户登录的最后10个IP，在models被import时执行。"""
        entry = ExtraProfileEntry()
        entry.name = 'login IP'  # 记录login的IP 
        entry.source = 'M'       # 从request.META读出
        entry.time = 'I'         # 每次login时记录
        entry.type = "IPAddressField" 
        entry.dupli = 10         # 记录最近10次的IP
        entry.keyword = 'REMOTE_ADDR' # 记录request.META['REMOTE_ADDR']
        entry.save()
except Exception, error:
    pass

