#from __future__ import unicode_literalss
from django.db import models

# Create your models here.
# class user(models.Model):
#     username = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)
#
#     # 此函数是为了用该名字来显示对象
#     def __unicode__(self):
#         return self.username
from django.contrib.auth.models import User


# 继承与django默认的User模型
class webinfoUser(User):
    # 添加两个字段，分别是登录日期和注册日期（自动填入）
    logindate = models.DateField(auto_now=True)
    registerdate = models.DateField(auto_now_add=True)