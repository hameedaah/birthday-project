from rest_framework import viewsets, permissions
from .models import Birthday, User
from .serializers import BirthdaySerializer, UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema

class BirthdayViewSet(viewsets.ModelViewSet):
    queryset = Birthday.objects.all()
    serializer_class = BirthdaySerializer
    authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=BirthdaySerializer)
    def create(self, request, *args, **kwargs):
        return super(BirthdayViewSet, self).create(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]

    permission_classes = [permissions.IsAuthenticated]  # or a custom permission

    @swagger_auto_schema(request_body=UserSerializer)
    def create(self, request, *args, **kwargs):
        """
        Create a new user without a password.
        """
        return super().create(request, *args, **kwargs)