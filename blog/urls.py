from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^index/$', views.index_view, name='index'),
    url(r'^article/(?P<article_id>[0-9]+)/$', views.detail_view, name='article_detail'),
    url(r'^new_article/$', views.new_article_view, name='new_article_view'),
    url(r'^do_new_category/$', views.do_new_category, name='do_new_category'),
    url(r'^do_create_article/$', views.do_create_article, name='do_create_article'),
    url(r'^articles/category/(?P<category_id>[0-9]+)/$', views.do_show_articles_by_category, name='do_show_articles_by_category'),
    url(r'^articles/tag/(?P<tag_id>[0-9]+)/$', views.do_show_articles_by_tag, name='do_show_articles_by_tag'),
    url(r'^admin/$', views.admin_view, name='admin_view'),

]