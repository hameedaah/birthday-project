from rest_framework import serializers
from .models import Staff, NotificationTemplate, NotificationLog
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
    staff = StaffSerializer(read_only=True)
    class Meta:
        model = NotificationTemplate
        fields = '__all__'
        read_only_fields = ['staff', 'id','created_at', 'updated_at']

class NotificationLogSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True)
    class Meta:
        model = NotificationLog
        fields = '__all__'
        read_only_fields = ['staff', 'id','status','error_message','created_at']

