from rest_framework import serializers
from .models import Staff, NotificationTemplate
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

class StaffSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def validate_first_name(self, value):
        return value.capitalize()

    def validate_last_name(self, value):
        return value.capitalize()
    

      
    class Meta:
        model = Staff
        fields = '__all__'
        read_only_fields = ['id','created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id']

class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = '__all__'
        read_only_fields = [Staff, 'id','created_at', 'updated_at']