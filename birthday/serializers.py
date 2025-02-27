from rest_framework import serializers
from .models import Staff, NotificationTemplate, NotificationLog
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .utils import send_email

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

class UserForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            User.objects.get(email=email, is_staff=True, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"Admin with email address: {email} does not exist.")
        return email

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email, is_staff=True, is_active=True)
        
        # Generate token using Django's default token generator
        token = default_token_generator.make_token(user)
        
        # Encode the user's UUID into a URL-safe base64 string (uidb64)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Construct the password reset URL
        reset_link = f"https://birthday-app-group-8.vercel.app/reset-password?uid={uidb64}&token={token}"
        

        subject = "Reset Your Account Password"
        html_content = (
            "<p>Hello,</p>"
            "<p>You requested a password reset for your staff account.</p>"
            f"<p>Please click the link below to reset your password:</p>"
            f"<p><a href='{reset_link}'>Reset Password</a></p>"
            "<p>If you did not request this, please ignore this email.</p>"
        )

        send_email(
            to_email=user.email,
            subject=subject,
            html_content=html_content,
        )

class UserResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        uidb64 = attrs.get('uid')
        token = attrs.get('token')
        new_password = attrs.get('new_password')

        try:
            uid = urlsafe_base64_decode(uidb64).decode()  # Decode the uid
        except Exception:
            raise serializers.ValidationError("Invalid UID.")


        User = get_user_model()
        # Retrieve user by UUID
        try:
            user = User.objects.get(pk=uid, is_staff=True, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid admin.")

        # Check token validity
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError("Invalid or expired token.")

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user

