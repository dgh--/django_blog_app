"""
    Url conf for blog application.
"""

from django.conf.urls import url
from django.conf.urls import include 

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index_view, name = 'index'),

    url(r'^(?P<pk>[0-9]+)/data/$', views.post_data_view, name = 'post_data'),
    url(r'^create_post/$', views.create_post_view, name = 'create_post'),
    url(r'(?P<pk>[0-9]+)/delete_post/', views.delete_post_view, name = 'delete_post'),

    url(r'^(?P<post_pk>[0-9]+)/delete/(?P<comment_pk>[0-9]+)/$', views.delete_comment_view, name = 'delete_comment'),

    url(r'^logout/$', views.logout_view, name = 'logout'),
]
