try:
    from django.conf.urls import patterns, include, url
except ImportError:
    from django.conf.urls.defaults import patterns, include, url

# URL test patterns for unitology. Use this file to ensure a consistent
# set of URL patterns are used when running unit tests. This test_urls
# module should be referred to by your test class.

urlpatterns = patterns('',
    url(r'^unitology/', include('unitology.urls')),
)
