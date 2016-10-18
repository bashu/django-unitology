# -*- coding: utf-8 -*-

try:
    from django.conf.urls import include, url
except ImportError:
    from django.conf.urls.defaults import include, url

from . import views

urlpatterns = [
    url(r'^reload/$', views.reload, name='unitology_reload'),
]
