from rest_framework import serializers
from .models import Birthday, Staff
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'
        read_only_fields = ['id','created_at', 'updated_at']

class BirthdaySerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True)
    def validate_date_of_birth(self, value):
        # Ensure the date is in the past
        if value > datetime.today().date():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    class Meta:
        model = Birthday
        fields = '__all__'
        read_only_fields = ['id', 'staff', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id']
