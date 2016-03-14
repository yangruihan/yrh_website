from django.shortcuts import render
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def index_view(request):
    """
    主页
    """
    return render(request, 'main/index.html')

def register_view(request):
    """
    注册页面
    """
    return render(request, 'main/register.html')

def register_suc_view(request):
    """
    注册成功页面
    """
    return render(request, 'main/register_suc.html')


def register_fail_view(request):
    """
    注册失败页面
    """
    return render(request, 'main/register_fail.html')

def username_check_aciton(request):
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

def do_register_aciton(request):
    """
    注册
    """
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['logged_in_user'] = user
            else:
                return HttpResponseRedirect(reverse('register_fail'))
        else:
            return HttpResponseRedirect(reverse('register_fail'))
    except KeyError as e:
        print(e)
        return HttpResponseRedirect(reverse('register_fail'))
    else:
        return HttpResponseRedirect(reverse('register_suc'))

def do_logout_aciton(request):
    """
    用户注销
    """
    try:
        del request.session['logged_in_user']
        logout(request)
    except KeyError as e:
        print(e)
    return HttpResponseRedirect("/")

def login_view(request):
    """
    登录页面
    """
    return render(request, 'main/login.html')


def do_login_aciton(request):
    """
    登录
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            request.session['logged_in_user'] = user
            return HttpResponseRedirect("/")
        else:
            return render(request, 'main/login.html',
                          {'username': user.username,
                           'error_message': "登录失败，用户名或密码错误"})
    else:
        return render(request, 'main/login.html',
                      {'error_message': "登录失败，用户名不存在"})