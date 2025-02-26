from django.contrib import admin
from django.urls import include, path
from .views import StaffViewSet, AdminLoginView, DepartmentListView, NotificationLogListView, NotificationTemplateRetrieveUpdateView, NotificationLogByStaffListView
from rest_framework.routers import DefaultRouter

staff_router = DefaultRouter()

staff_router.register(r'admin/staff', StaffViewSet, basename='staff')



urlpatterns = [
    path("api/", include([
        path("auth/login/", AdminLoginView.as_view(), name="admin-login"),
        path("departments/", DepartmentListView.as_view(), name="departments-list"),
        path('admin/notification-template/<uuid:staff_id>/', NotificationTemplateRetrieveUpdateView.as_view(), name='notification-template'),
        path('api/admin/notification-logs/', NotificationLogListView.as_view(), name='notification-log-list'),
        path('api/admin/notification-logs/<uuid:staff_id>/', NotificationLogByStaffListView.as_view(), name='notification-log-list-by-staff'),
        path("", include(staff_router.urls)), 
    ])),
]
