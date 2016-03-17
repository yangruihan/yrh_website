from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

import datetime
import time
import json
from collections import OrderedDict

from .models import Task
from calendar import month

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

@csrf_protect
@login_required(login_url='/login')
def api_get_task_statistics_calendar_data(request):
    """
    任务完成情况api
    """
    user = request.user
    # 得到该用户所有已完成任务
    completed_tasks = Task.objects.filter(user=user).filter(have_completed=True)
    result = {}
    for completed_task in completed_tasks:
        if str(time.mktime(completed_task.done_date.timetuple())) not in completed_tasks:
            result[str(time.mktime(completed_task.done_date.timetuple()))] = 1
        else:
            result[str(time.mktime(completed_task.done_date.timetuple()))] += 1
    result_json = json.dumps(result)
    return HttpResponse(result_json, content_type="application/json")

@login_required(login_url='/login')
def api_get_completed_tasks_num_last_year(request):
    """
    获得一年内该用户完成的任务次数
    """
    user = request.user
    now_date = timezone.now()
    last_year_date = now_date - datetime.timedelta(days=365)
    completed_tasks_num_last_year = Task.objects.filter(user=user,
                                                        have_completed=True, 
                                                        done_date__gte=last_year_date,
                                                        done_date__lte=now_date)
    result = {'completed_tasks_num_last_year': completed_tasks_num_last_year.count()}
    result_json = json.dumps(result)
    return HttpResponse(result_json, content_type="application/json")

@login_required(login_url='/login')
def api_get_last_year_to_now_date_string(request):
    """
    获得去年到今年日期的字符串
    """
    now_date = timezone.now()
    last_year_date = now_date - datetime.timedelta(days=365)
    result = {'during_date_string': '%s/%s/%s - %s/%s/%s' % (last_year_date.year,
                                                             last_year_date.month,
                                                             last_year_date.day,
                                                             now_date.year,
                                                             now_date.month,
                                                             now_date.day)}
    result_json = json.dumps(result)
    return HttpResponse(result_json, content_type="application/json")

@login_required(login_url='/login')
def api_get_longest_streak_days_number(request):
    """
    获得最长坚持天数
    """
    user = request.user
    completed_tasks = Task.objects.filter(user=user,
                                          have_completed=True).order_by('done_date')
    longest_days = 1
    now_days = 1
    now_date = datetime.date(completed_tasks[0].done_date.year,
                             completed_tasks[0].done_date.month,
                             completed_tasks[0].done_date.day)
    result = {}
    for i in range(1, completed_tasks.count()):
        temp_date = datetime.date(completed_tasks[i].done_date.year,
                                  completed_tasks[i].done_date.month,
                                  completed_tasks[i].done_date.day)
        if now_date == temp_date - datetime.timedelta(days=1):
            now_days += 1
        elif now_date < temp_date - datetime.timedelta(days=1):
            if now_days > longest_days:
                longest_days = now_days
            now_days = 1
            
        now_date = temp_date
    
    result['longest_streak_days_number'] = longest_days if longest_days > now_days else now_days
    result_json = json.dumps(result)
    return HttpResponse(result_json, content_type="application/json")

@login_required(login_url='/login')
def api_get_current_streak_days_number(request):
    """
    获得目前坚持天数
    """
    user = request.user
    completed_tasks = Task.objects.filter(user=user,
                                          have_completed=True)
    now_days = 1
    now_date = datetime.date(completed_tasks[completed_tasks.count() - 1].done_date.year,
                             completed_tasks[completed_tasks.count() - 1].done_date.month,
                             completed_tasks[completed_tasks.count() - 1].done_date.day)
    
    result = {}
    if now_date != datetime.date.today():
        result['current_streak_days_number'] = 0
        result_json = json.dumps(result)
        return HttpResponse(result_json, content_type="application/json")
    
    for i in range(completed_tasks.count() - 1, 0, -1):
        temp_date = datetime.date(completed_tasks[i].done_date.year,
                                  completed_tasks[i].done_date.month,
                                  completed_tasks[i].done_date.day)
        if now_date == temp_date + datetime.timedelta(days=1):
            now_days += 1
        elif now_date > temp_date + datetime.timedelta(days=1):
            break
        
    result['current_streak_days_number'] = now_days
    result_json = json.dumps(result)
    return HttpResponse(result_json, content_type="application/json")

def get_completed_tasks_status(key, user):
    """
    获得完成任务情况
    key == 'week' 表示获得一周内完成情况
    key == 'month' 表示获得一个月内完成情况
    key == 'day' 表示一天内完成情况
    key == '3day' 表示3天内完成情况
    """
    now_date = timezone.now()
    if key == 'week':
        last_date = now_date - datetime.timedelta(days=7)
    elif key == 'day':
        last_date = now_date - datetime.timedelta(days=1)
    elif key == '3day':
        last_date = now_date - datetime.timedelta(days=3)
    elif key == 'month':
        last_date = now_date - datetime.timedelta(days=30)
        
    completed_tasks_num_last_week = Task.objects.filter(user=user,
                                                        have_completed=True, 
                                                        done_date__gte=last_date,
                                                        done_date__lte=now_date)
    result = OrderedDict()
    for task in completed_tasks_num_last_week:
        result[str(timezone.localtime(task.done_date)).split('+')[0]] = task.content
        
    result_json = json.dumps(result)
    return result_json
    
@login_required(login_url='/login')
def api_get_completed_tasks_status_week(request):
    return HttpResponse(get_completed_tasks_status('week', request.user), content_type="application/json")

@login_required(login_url='/login')
def api_get_completed_tasks_status_day(request):
    return HttpResponse(get_completed_tasks_status('day', request.user), content_type="application/json")

@login_required(login_url='/login')
def api_get_completed_tasks_status_3day(request):
    return HttpResponse(get_completed_tasks_status('3day', request.user), content_type="application/json")

@login_required(login_url='/login')
def api_get_completed_tasks_status_month(request):
    return HttpResponse(get_completed_tasks_status('month', request.user), content_type="application/json")



