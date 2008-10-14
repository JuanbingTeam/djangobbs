#coding=utf-8
#!/usr/bin/env python

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext as _T 

class Province(models.Model):
    """省/直辖市"""
    fullname = models.CharField(max_length=100, db_index=True)      # 全称。如北京市，内蒙古自治区，江苏
    shortname = models.CharField(max_length=10, db_index=True)      # 简单名称，比如上海市简称上海，内蒙古自治区简称内蒙古
    abbreviation = models.CharField(max_length=3, db_index=True)    # 单字简称，如沪、浙
    
    def __unicode__(self):
        return self.fullname
    
admin.site.register(Province)
    
class City(models.Model):
    """市/县/区"""
    fullname = models.CharField(max_length=50, db_index=True)       # 名称
    province = models.ForeignKey(Province)                          # 所属省、市
    telcode = models.CharField(max_length = 3, db_index=True)       # 电话区号
    def __unicode__(self):
        return unicode(self.province) + self.fullname
    
admin.site.register(City)

class Address(models.Model):
    """地址"""
    city = models.ForeignKey(City)                                  # 城市 
    street = models.TextField(blank=True, default="")               # 街道
    address = models.TextField(blank=True, default="")              # 详细地址
    zipcode = models.CharField(max_length = 10, blank=True, db_index=True)  # 邮政编码
    telphone = models.CharField(max_length = 20, blank=True, db_index=True) # 电话号码（不需要区号）
    def __unicode__(self):
        return unicode(self.city) + self.street + self.address

admin.site.register(Address)

class EMail(models.Model):
    """电子邮件"""
    email = models.EmailField(db_index=True)                        # 电子邮件地址                    
    note = models.TextField(blank=True, default="")                 # 说明
    
    def __unicode__(self):
        return self.email

admin.site.register(EMail)

class InternetMessager(models.Model):
    """网络通讯工具"""
    INTERNET_MESSAGER_CHOICES = (("M", "MSN"), ("Q", "QQ"), ("I", "ICQ"), ("Y", "Yahoo Messsager"), ("O", "Others"))
    type = models.CharField(max_length = 1, choices = INTERNET_MESSAGER_CHOICES)    # 类型
    code = models.CharField(max_length=200, db_index=True)                          # 号码

    def __unicode__(self):
        return self.type + self.code
     
admin.site.register(InternetMessager)

class Person(models.Model):
    """个人信息"""
    SEX_CHOICES = (('M', 'Male'), ('F', 'Female'), ('X', 'Unknown'))    # 性别类型
    firstName = models.CharField(max_length=50, db_index=True)          # 姓
    middleName = models.CharField(max_length=50, db_index=True, blank=True, default="") # 中间名
    lastName = models.CharField(max_length=50, db_index=True)           # 名
    title = models.CharField(max_length=50, db_index=True, blank=True, default="")  # 头衔
    
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='X')           # 性别
    birthday = models.DateField(null=True, blank=True, default=None)                                       # 生日
    
    family = models.ForeignKey(Address, related_name='family_address', null=True, blank=True, default=None)   # 家庭住址
    
    organization = models.ForeignKey('Organization', null=True, blank=True, default=None)           # 所属单位
    department = models.TextField(blank=True, default="")                                           # 所在部门
    officeAddress = models.ForeignKey(Address, related_name='work_address', null=True, blank=True, default=None)     # 单位地址
    
    messagers = models.ManyToManyField(InternetMessager, blank=True)                # 网络通讯
    otherEmails = models.ManyToManyField(EMail, blank=True, related_name='other_emails')    # 电子信息 
    defaultEmail = models.ForeignKey(EMail, null=True, blank=True, default=None)
    blog = models.URLField(blank=True, default="", verify_exists=False) # 个人BLOG

    note = models.TextField(blank=True, default="")                     # 其它说明
    
    def __unicode__(self):
        return self.firstName + self.middleName + self.lastName + self.title
        
admin.site.register(Person)

class Organization(models.Model):
    """单位、组织"""
    name = models.CharField(max_length = 20, db_index=True)                         # 名称
    address = models.ForeignKey(Address, null=True, blank=True)                     # 地址
    boss = models.ForeignKey(Person, related_name='boss', null=True, blank=True)    # 老板
    fax = models.CharField(max_length = 20, blank=True, default="", db_index=True)  # 传真
    homepage = models.URLField(blank=True, default="", verify_exists=False)         # 公司主页
    employees = models.ManyToManyField(Person, blank=True, related_name='empolyees')# 员工 
    note = models.TextField(blank=True, default="")                                 # 其它说明
    
    def __unicode__(self):
        return self.name
    
admin.site.register(Organization)
