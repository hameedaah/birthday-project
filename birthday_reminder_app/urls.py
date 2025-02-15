from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("birthday/", include("birthday.urls")),
    path("admin/", admin.site.urls),
]