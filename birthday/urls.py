from django.contrib import admin
from django.urls import include, path


from .views import BirthdayViewSet, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'birthdays', BirthdayViewSet, basename='birthday')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]