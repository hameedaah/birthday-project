from rest_framework import serializers
from .models import Staff
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

class StaffSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    def get_first_name(self, obj):
        return obj.first_name.capitalize() 

    def get_last_name(self, obj):
        return obj.last_name.capitalize() 
    

      
    class Meta:
        model = Staff
        fields = '__all__'
        read_only_fields = ['id','created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id']
