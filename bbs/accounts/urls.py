#coding=utf-8
#!/usr/bin/env python

from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
    (r'^$', 'index'),               # "用户主页"
    (r'^(?P<id>\d+)/$', 'index'),   # "用户主页"
    (r'^login/', 'login'),          # "登陆"
    (r'^logout/', 'logout'),        # "登出"
    (r'^register/', 'register'),    # "注册"
    (r'^password/', 'password'),    # "修改密码"
    (r'^reset/', 'resetPassword'),  # "重置密码"
    (r'^validate/', 'validate'),    # "获取验证码"
)