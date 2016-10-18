# -*- coding: utf-8 -*-

try:
    from django.conf.urls import patterns, include, url
except ImportError:
    from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('unitology.views',
    url(r'^reload/$', 'reload', name='unitology_reload'),
)
