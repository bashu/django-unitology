from django.conf.urls import include, re_path
from django.contrib import admin

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
]

urlpatterns += [
    re_path(r"^unitology/", include("unitology.urls")),
]
