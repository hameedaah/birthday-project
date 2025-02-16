# serializers.py
from rest_framework import serializers
from .models import Birthday

# serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
        ]
        # Typically, the 'id' might be UUID if you're using a custom user with UUID primary key
        # 'read_only_fields' can be used to disallow modification of certain fields
        read_only_fields = ['id']

class BirthdaySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Birthday
        fields = ['id','user', 'created_at', 'birth_date', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
