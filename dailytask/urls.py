from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_task/$', views.add_task, name='add_task'),
    url(r'^update_task/$', views.update_task, name='update_task'),
    url(r'^delete_task/$', views.delete_task, name='delete_task'),
    url(r'^change_task_status/$', views.change_task_status, name='change_task_status'),
]