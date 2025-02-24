from django.contrib import admin
from django.urls import include, path
from .views import StaffViewSet, AdminLoginView, DepartmentListView
from rest_framework.routers import DefaultRouter

staff_router = DefaultRouter()
staff_router.register(r'admin/staff', StaffViewSet, basename='staff')

urlpatterns = [
    path("api/", include([
        path("departments/", DepartmentListView.as_view(), name="departments-list"),
        path("auth/login/", AdminLoginView.as_view(), name="admin-login"),
        path("", include(staff_router.urls)), 
    ])),
]