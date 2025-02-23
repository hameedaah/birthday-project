from rest_framework import viewsets, permissions, status
from .models import Staff, User
from .serializers import  StaffSerializer, UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import IntegerField, Case, When, Value, F
from datetime import date


class AdminLoginView(APIView):
    @swagger_auto_schema(
        operation_description="Admin login endpoint.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="Admin email"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="Admin password"),
            },
            required=['email', 'password']
        ),
        responses={
            200: openapi.Response(description="Successful login"),
            403: openapi.Response(description="Access denied - Not an admin"),
            401: openapi.Response(description="Invalid email or password"),
        }
    )

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        request.data['username'] = request.data.pop('email')
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_staff:  
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name
                    }
                }, status=status.HTTP_200_OK)
            return Response({"detail": "Access denied. You do not have admin privileges."}, status=status.HTTP_403_FORBIDDEN)
        return Response({"detail": "Invalid email or password. Please check your credentials and try again."}, status=status.HTTP_401_UNAUTHORIZED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser] 

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    # Define authentication method
    authentication_classes = [JWTAuthentication]
    # Only authenticated users can access
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_permissions(self):
        """Allow unauthenticated access for GET, require authentication for others"""
        if self.action in ['list', 'retrieve']:  # Public access for GET requests
            return [permissions.AllowAny()]
        return super().get_permissions()
    

    def get_queryset(self):
        today = date.today()
        return Staff.objects.annotate(
            # Extract month and day from date_of_birth
            birth_month=F('date_of_birth__month'),
            birth_day=F('date_of_birth__day'),
            # Determine if the birthday has passed in the current year
            birthday_passed=Case(
                When(
                    birth_month__lt=today.month, then=Value(1)
                ),
                When(
                    birth_month=today.month, birth_day__lt=today.day, then=Value(1)
                ),
                default=Value(0),
                output_field=IntegerField()
            )
        ).order_by('birthday_passed', 'birth_month', 'birth_day')  # ✅ Upcoming birthdays first



    @swagger_auto_schema(
        operation_description="Return a list of all staff.",
        responses={200: StaffSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Accept staff details and create a new staff.",
        request_body=StaffSerializer,
        responses={201: StaffSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Fetch a single staff based on their id.",
        responses={200: StaffSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an existing staff based on their id.",
        request_body=StaffSerializer,
        responses={200: StaffSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Removes a staff the database based on their id.",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)