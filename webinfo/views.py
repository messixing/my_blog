import importlib,sys
importlib.reload(sys)
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from webinfo.models import webinfoUser
from PIL import Image,ImageDraw,ImageFont
from random import randint
# 导入StringIO模块
from io import StringIO
from io import BytesIO
# 这里新导入了一个HttpResponseRedirect函数，用于页面的重定向
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.contrib import auth
# 在django中权限就是一个Permission模型的实例
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
import json
# def home(request):
#     return HttpResponse('小白炸了！')

# def query(request):  # 新添加的查询接口
#     name = request.GET['name']  # 查询GET方法传过来的name参数
#     time = request.GET['time']  # 查询GET方法传过来的time参数
#     return HttpResponse("Good " + time + ', ' + name + '.')

def index(request):
    return render(request, 'index.html')
def linktologin(request):
    return render(request, 'user/login.html')
def linktoreg(request):
    return render(request, 'user/reg.html')
def setuserhomepage(request):
    return render(request, 'user/set.html')
# 使用装饰器，在函数前@这个装饰器
# 参数login_url为没有登录的时候需要跳转到哪里，这里设置为跳转到首页
# 参数redirect_field_name为重定向时传输当前的页面路径，这里设置为没有
@login_required(login_url='/', redirect_field_name=None)
def user(request):
     # 不再需要判断是否已经登录了
     return render(request, 'user/home.html')
@csrf_protect

def logout(request):
    # 登出设置，并重定向到首页
    auth.logout(request)
    return HttpResponseRedirect('/')


def check(request):
    if request.POST['verify'].lower() == request.session['verify'].lower():
        password = request.POST['pass']
        username = request.POST['username']
        if request.POST['way'] == 'login':
            # 这里修改为直接返回函数返回的值
            return login(request, username, password)
        elif request.POST['way'] == 'register':
            email = request.POST['email']
            return register(request,email, username, password)
    else:
        return HttpResponse('验证码错误')


def login(request,username, password):
    try:
        # 使用webinfoUser模型获取用户
        guest = webinfoUser.objects.get(username=username)
        user = auth.authenticate(username=username, password=password)
        if user is None:
            return HttpResponse('密码错误')
        else:
            auth.login(request, user)
            # 输出我们之前新添加的两个属性（懒的在页面上显示了）
            return HttpResponseRedirect('/user?username=' + username)
    except:
        return HttpResponse('不存在该用户')



def verify(request, width, height):
    wordsCount = 4
    width = int(width)
    height = int(height)
    size = int(min(width / wordsCount, height) / 1.3)
    bgColor = (randint(200, 255), randint(200, 255), randint(200, 255))
    img = Image.new('RGB', (width, height), bgColor)
    font = ImageFont.truetype('/static/Arial.ttf', size)
    draw = ImageDraw.Draw(img)
    text = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    verifytext = ''
    for i in range(wordsCount):
        textColor = (randint(0, 160), randint(0, 160), randint(0, 160))
        left = width * i / wordsCount + (width / 4 - size) / 2
        top = (height - size) / 2
        word = text[randint(0, len(text) - 1)]
        verifytext += word
        draw.text((left, top), word, font=font, fill=textColor)
    for i in range(30):
        textColor = (255, 255, 255)
        left = randint(0, width)
        top = randint(0, height)
        draw.text((left, top), '*', font=font, fill=textColor)
    for i in range(5):
        linecolor = (randint(0, 160), randint(0, 160), randint(0, 160))
        line = (randint(0, width), randint(0, height), randint(0, width), randint(0, height))
        draw.line(line, fill=linecolor)
    del draw
    mstream = BytesIO()
    img.save(mstream, 'jpeg')
    request.session['verify'] = verifytext
    print(verifytext)
    return HttpResponse(mstream.getvalue(), 'image/jpeg')


def get_or_create_group(name, permissions=None):
    group = Group.objects.get_or_create(name=name)[0]
    if permissions:
        permissions_codename = [i.codename for i in group.permissions.all()]
        for i in permissions:
            if i not in permissions_codename:
                group.permissions.add(Permission.objects.get_or_create(**{
                    'codename': i,
                    'name': ' '.join(i.split('_')).title(),
                    'content_type': ContentType.objects.get_for_model(webinfoUser)
                })[0])
    return group


def group_required(group, **kwargs):
    def check_group(user):
        return set(groups).issubset(set([i.name for i in user.groups.all()]))

    groups = group if isinstance(group, (list, tuple)) else (group,)
    # 这个函数用于跳转，check_group判断是否存在组，然后返回布尔值
    return user_passes_test(check_group, **kwargs)

    # 组的装饰器都写了，就不介意自己写一个权限的装饰器吧


def permission_required(perm, **kwargs):
    perms = perm if isinstance(perm, (list, tuple)) else (perm,)
    return user_passes_test(lambda user: user.has_perms(perms), **kwargs)


# 必须是拥有组manager的用户才可以访问
@group_required('manager', login_url='/', redirect_field_name=None)
def manager(request):
    return render(request, 'manager.html')


# 必须是拥有webinfo.show_all_user权限的才可以访问
@permission_required('webinfo.show_all_user', login_url='/', redirect_field_name=None)
def show_all_user(request):
    return HttpResponse(json.dumps([i.username for i in webinfoUser.objects.all()]))


def register(request,email, username, password):
    try:
        user = webinfoUser.objects.create_user(email=email,username=username, password=password)
        user.groups = [get_or_create_group('manager', permissions=['show_all_user'])]
        user.save()
        login(request,username, password)
        return HttpResponseRedirect('/user?username=' + username)
    except:
        return HttpResponse('已存在用户')
