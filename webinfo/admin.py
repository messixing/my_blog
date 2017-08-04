from django.contrib import admin
# from webinfo.models import user
# # Register your models here.
# admin.site.register(user)# 把user添加到admin
from webinfo.models import webinfoUser
admin.site.register(webinfoUser)