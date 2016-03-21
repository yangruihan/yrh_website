from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^article/(?P<article_id>[0-9]+)$', views.detail_view, name='article_detail'),
    url(r'^new_article/$', views.new_article_view, name='new_article_view'),
    
]