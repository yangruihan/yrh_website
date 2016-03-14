from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

import datetime

from .models import Task

@login_required(login_url='/login')
def index_view(request):
    """
    主页
    """
    user = request.user
    now = timezone.now()
    create_date_where = ["Month(create_date)='%s'" % now.month, "Day(create_date)='%s'" % now.day]
    done_date_where = ["Month(done_date)='%s'" % now.month, "Day(done_date)='%s'" % now.day]
    uncompleted_tasks = Task.objects.filter(user=user).filter(have_completed=False).extra(where=create_date_where)
    completed_tasks = Task.objects.filter(user=user).filter(have_completed=True).extra(where=done_date_where)
    return render(request, 'dailytask/index.html', 
        {'uncompleted_tasks': uncompleted_tasks,
         'completed_tasks': completed_tasks})

@csrf_protect
@login_required(login_url='/login')
def add_task_action(request):
    """
    添加任务到数据库
    """
    try:
        user = request.user
        task_content = request.POST["content"]
        task = Task(user=user, content=task_content)
        task.save()
        return HttpResponse(task.id)
    except Exception as e:
        print(e)
        return HttpResponse('fail')

@csrf_protect
@login_required(login_url='/login')
def update_task_action(request):
    """
    修改任务内容
    """
    try:
        id = int(request.POST["id"])
        task = Task.objects.get(pk=id)
        task.content = request.POST["content"]
        task.save()
        return HttpResponse('success')
    except Exception as e:
        print(e)
        return HttpResponse('fail')

@csrf_protect
@login_required(login_url='/login')
def delete_task_action(request):
    """
    删除某条任务
    """
    try:
        id = int(request.POST["id"])
        Task.objects.get(pk=id).delete()
        return HttpResponse('success')
    except Exception as e:
        print(e)
        return HttpResponse('fail')

@csrf_protect
@login_required(login_url='/login')
def change_task_status_action(request):
    """
    完成某条任务
    """
    try:
        id = int(request.POST["id"])
        task = Task.objects.get(pk=id)
        if (request.POST['action'] == 'finish'):
            task.done_date = timezone.now()
            task.have_completed = True
        else:
            task.have_completed = False
        task.save()
        return HttpResponse('success')
    except Exception as e:
        print(e)
        return HttpResponse('fail')
