"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from webinfo.views import index
from webinfo.views import user
from webinfo.views import verify
from webinfo.views import check
from webinfo.views import logout
from webinfo.views import manager
from webinfo.views import show_all_user
from webinfo.views import linktologin
from webinfo.views import linktoreg
from webinfo.views import setuserhomepage


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),  # 可以使用设置好的url进入网站后台
    url(r'^$', index),
    url(r'^user$', user),
    url(r'^linktologin$', linktologin),
    url(r'^linktoreg$', linktoreg),
    url(r'^setuserhomepage$', setuserhomepage),
    url(r'^verify/(\d+)/(\d+)/$', verify),
    url(r'^check/$', check),
    url(r'^logout/$', logout),
    url(r'^manager$', manager),
    url(r'^show_all_user/$', show_all_user),
]
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
# from django.conf.urls import patterns, include, url
# from django.contrib import admin
#
# urlpatterns = patterns('',
#     # Examples:
#     # url(r'^
#     url(r'^admin/', include(admin.site.urls)),  #可以使用设置好的url进入网站后台
#     url(r'^$', 'article.views.home'),
# )