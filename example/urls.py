from django.conf.urls import include, url
from django.contrib import admin

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += [
    url(r'^unitology/', include('unitology.urls')),
]
