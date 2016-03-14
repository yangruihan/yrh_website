from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^add_task/$', views.add_task_action, name='add_task'),
    url(r'^update_task/$', views.update_task_action, name='update_task'),
    url(r'^delete_task/$', views.delete_task_action, name='delete_task'),
    url(r'^change_task_status/$', views.change_task_status_action, name='change_task_status'),
]