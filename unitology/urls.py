# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('unitology.views',
    url(r'^reload/$', 'reload', name='unitology_reload'),
)
