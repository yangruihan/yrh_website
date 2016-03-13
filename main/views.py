from django.shortcuts import render
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from .models import User

def index(request):
    """
    主页
    """
    return render(request, 'main/index.html')

def register(request):
    """
    注册页面
    """
    return render(request, 'main/register.html')

def register_suc(request):
    """
    注册成功页面
    """
    return render(request, 'main/register_suc.html')


def register_fail(request):
    """
    注册失败页面
    """
    return render(request, 'main/register_fail.html')

def username_check(request):
    """
    用户名检测
    """
    try:
        if request.GET['username'].strip() == '':
            return HttpResponse("请输入用户名")
        else:
            User.objects.get(username=request.GET['username'])
            return HttpResponse("用户名已存在，请重新输入")
    except User.DoesNotExist:
        return HttpResponse("")

def do_register(request):
    """
    注册
    """
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User(username=username, password=password,
                    email=email, create_date=timezone.now())
        user.save()
        request.session['logged_in_user'] = user
    except KeyError as e:
        print(e)
        return HttpResponseRedirect(reverse('register_fail'))
    else:
        return HttpResponseRedirect(reverse('register_suc'))

def do_logout(request):
    """
    用户注销
    """
    try:
        del request.session['logged_in_user']
    except KeyError as e:
        print(e)
    return HttpResponseRedirect("/")

def login(request):
    """
    登录页面
    """
    return render(request, 'main/login.html')


def do_login(request):
    """
    登录
    """
    try:
        user = User.objects.get(username=request.POST['username'])
        if user.password == request.POST['password']:
            request.session['logged_in_user'] = user
            return HttpResponseRedirect("/")
        else:
            return render(request, 'main/login.html',
                          {'username': user.username,
                           'error_message': "登录失败，用户名或密码错误"})
    except (KeyError, User.DoesNotExist):
        return render(request, 'main/login.html',
                      {'error_message': "登录失败，用户名不存在"})