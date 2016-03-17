from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^add_task/$', views.add_task_action, name='add_task'),
    url(r'^update_task/$', views.update_task_action, name='update_task'),
    url(r'^delete_task/$', views.delete_task_action, name='delete_task'),
    url(r'^change_task_status/$', views.change_task_status_action, name='change_task_status'),
    url(r'^api/get_task_statistics_calendar_data/$', views.api_get_task_statistics_calendar_data, name='api_get_task_statistics_calendar_data'),
    url(r'^api/get_completed_tasks_num_last_year/$', views.api_get_completed_tasks_num_last_year, name='api_get_completed_tasks_num_last_year'),
    url(r'^api/get_last_year_to_now_date_string/$', views.api_get_last_year_to_now_date_string, name='api_get_last_year_to_now_date_string'),
    url(r'^api/get_longest_streak_days_number/$', views.api_get_longest_streak_days_number, name='api_get_longest_streak_days_number'),
    url(r'^api/get_current_streak_days_number/$', views.api_get_current_streak_days_number, name='api_get_current_streak_days_number'),
    
]