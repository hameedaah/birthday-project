from django.contrib import admin
from django.urls import include, path
from .views import StaffViewSet, AdminLoginView
from rest_framework.routers import DefaultRouter


staff_router = DefaultRouter()
staff_router.register(r'api/admin/staff', StaffViewSet, basename='staff')



urlpatterns = [
    path('api/auth/login/', AdminLoginView.as_view(), name='admin-login'),
    path('', include(staff_router.urls)),  
]

