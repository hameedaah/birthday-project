from django.contrib import admin
from django.urls import include, path
from .views import BirthdayViewSet, StaffViewSet, AdminLoginView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'birthday', BirthdayViewSet, basename='birthday')
staff_router = DefaultRouter()
staff_router.register(r'staff', StaffViewSet, basename='staff')



urlpatterns = [
    path('api/auth/login/', AdminLoginView.as_view(), name='admin-login'),
    path('api/admin/', include(staff_router.urls)), 
    path('api/', include(router.urls)),  
]

