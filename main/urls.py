from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^register/', views.register_view, name='register'),
    url(r'^do_register/', views.do_register_aciton, name='do_register'),
    url(r'^username_check/', views.username_check_aciton, name='username_check'),
    url(r'^register_suc/', views.register_suc_view, name='register_suc'),
    url(r'^register_fail/', views.register_fail_view, name='register_fail'),
    url(r'^do_logout/', views.do_logout_aciton, name='do_logout'),
    url(r'^login', views.login_view, name='login'),
    url(r'^do_login/', views.do_login_aciton, name='do_login'),  
]