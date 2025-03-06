from django.contrib import admin
from django.urls import include, path
from .views import StaffViewSet, AdminLoginView, DepartmentListView, NotificationLogListView, NotificationTemplateRetrieveUpdateView, NotificationLogByStaffListView, UserForgotPasswordView,UserResetPasswordView, AdminProfileView
from rest_framework.routers import DefaultRouter

staff_router = DefaultRouter()

staff_router.register(r'admin/staff', StaffViewSet, basename='staff')



urlpatterns = [
    path("api/", include([
        #auth
        path("auth/login/", AdminLoginView.as_view(), name="admin-login"),
        path('auth/forgot-password/', UserForgotPasswordView.as_view(), name='staff_forgot_password'),
        path('auth/reset-password/', UserResetPasswordView.as_view(), name='staff_reset_password'),

        #admin
        # urls.py
        path('admin/profile/', AdminProfileView.as_view(), name='admin-profile'),



        #notification templates
        path('admin/notification-template/<uuid:staff_id>/', NotificationTemplateRetrieveUpdateView.as_view(), name='notification-template'),

        #notification logs
        path('admin/notification-logs/', NotificationLogListView.as_view(), name='notification-log-list'),
        path('admin/notification-logs/<uuid:staff_id>/', NotificationLogByStaffListView.as_view(), name='notification-log-list-by-staff'),

        #staff
        path("", include(staff_router.urls)), 

    	#departments
        path("departments/", DepartmentListView.as_view(), name="departments-list"),
    ])),
]
