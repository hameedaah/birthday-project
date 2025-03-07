from rest_framework import viewsets, permissions, status, filters, generics
from .models import Staff, User, NotificationTemplate, NotificationLog
from .serializers import  StaffSerializer, UserSerializer, NotificationTemplateSerializer, NotificationLogSerializer, UserForgotPasswordSerializer, UserResetPasswordSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import IntegerField, Case, When, Value, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError, NotFound
from datetime import date

DEPARTMENT_CHOICES = [
    "botany", "computer_science", "chemistry", "cell_biology_and_genetics",
    "marine_sciences", "mathematics", "microbiology", "physics",
    "statistics", "zoology"
]


class AdminLoginView(APIView):
    swagger_tags = ['auth']
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
        },
        tags = ['auth']
    )

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

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
                        "staff_id": user.staff_profile.id if hasattr(user, 'staff_profile') else None,
                        "email": user.email,
                        "profile_image_url": user.profile_image
                    }
                }, status=status.HTTP_200_OK)
            return Response(
                {
                    "message": "Access denied. You do not have admin privileges."
                }, status=status.HTTP_403_FORBIDDEN)
        return Response(
            {
                "message": "Invalid email or password. Please check your credentials and try again."
            }, status=status.HTTP_401_UNAUTHORIZED)

class AdminProfileView(APIView):
    swagger_tags = ['admin profile']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser] 

    @swagger_auto_schema(
        swagger_tags = ['admin profile'],
        operation_description="Retrieve the signed in admin's details.",
        responses={200: "Admin details returned successfully"}
    )
    def get(self, request):
        user = request.user  
        staff_id = None
        if hasattr(user, 'staff_profile'):
            staff_id = user.staff_profile.id

        return Response({
            "id": user.id,
            "email": user.email,
            "profile_image_url": user.profile_image, 
            "staff_id": staff_id,
        })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser] 

class StaffViewSet(viewsets.ModelViewSet):
    swagger_tags = ['staff']
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] 
    search_fields = ["first_name", "last_name", "department"]
    filterset_fields = ["department", "staff_type"]
    # Define authentication method
    authentication_classes = [JWTAuthentication]
    # Only authenticated users can access
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_permissions(self):
        """Allow unauthenticated access for GET, require authentication for others"""
        if self.action in ['list']:  
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    def get_queryset(self):
        today = date.today()
        queryset = Staff.objects.annotate(
            birth_month=F('date_of_birth__month'),
            birth_day=F('date_of_birth__day'),
            birthday_passed=Case(
                When(birth_month__lt=today.month, then=Value(1)),
                When(birth_month=today.month, birth_day__lt=today.day, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).order_by('birthday_passed', 'birth_month', 'birth_day')

        birth_month = self.request.query_params.get("birth_month")

        if birth_month:
            if not birth_month.isdigit(): 
                raise ValidationError({"birth_month": "Birth month must be a number between 1 and 12."})

            birth_month = int(birth_month) 
            
            if not (1 <= birth_month <= 12):  
                raise ValidationError({"birth_month": "Birth month must be between 1 and 12."})
            
            queryset = queryset.filter(date_of_birth__month=birth_month)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search staff by first name, last name, both or department",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "department",
                openapi.IN_QUERY,
                description="Filter staff by department",
                type=openapi.TYPE_STRING,
                enum=["botany", "computer_science", "chemistry", "cell_biology_and_genetics",
                      "marine_sciences", "mathematics", "microbiology", "physics",
                      "statistics", "zoology"],
            ),
            openapi.Parameter(
                "staff_type",
                openapi.IN_QUERY,
                description="Filter staff by staff type",
                type=openapi.TYPE_STRING,
                enum=["academic", "non_academic"],
            ),
            openapi.Parameter(
                "birth_month",
                openapi.IN_QUERY,
                description="Filter staff by birth month (1-12)",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: StaffSerializer(many=True),
            400: openapi.Response(
            description="Invalid birth month provided",
            examples={
                "application/json": {
                    "birth_month": "Birth month must be a number between 1 and 12.",
                    "staff_type": "Invalid staff type.",
                    "department": "Invalid department choice.",
                }
            }
            )
                   },
        tags = ['staff']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Accept staff details and create new staff.",
        request_body=StaffSerializer(many=True),  
        responses={201: StaffSerializer(many=True)},
        tags = ['staff']
    )
    def create(self, request, *args, **kwargs):
        """Handles both single and bulk staff creation"""
        data = request.data
        is_bulk = isinstance(data, list) 

        serializer = self.get_serializer(data=data, many=is_bulk)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Fetch a single staff based on their id.",
        responses={200: StaffSerializer},
        tags = ['staff']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an existing staff based on their id.",
        request_body=StaffSerializer,
        responses={200: StaffSerializer},
        tags = ['staff']
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Removes a staff the database based on their id.",
        responses={204: 'No Content'},
        tags = ['staff']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Update selected details of a staff member.",
        tags=['staff']
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

class DepartmentListView(APIView): 
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    swagger_tags = ['departments']

    @swagger_auto_schema(
        operation_description="Retrieve a list of all available departments",
        responses={200: openapi.Response(
            description="List of departments",
            examples={
                "application/json": [
                    "botany",
                    "computer_science",
                    "chemistry",
                    "cell_biology_and_genetics",
                    "marine_sciences",
                    "mathematics",
                    "microbiology",
                    "physics",
                    "statistics",
                    "zoology"
                ]
            }
        )},
        tags = ['departments']
    )
    def get(self, request):
        return Response(DEPARTMENT_CHOICES)

class NotificationTemplateRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    swagger_tags = ['notification template']
    serializer_class = NotificationTemplateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'put']

    def get_object(self):
        staff_id = self.kwargs.get('staff_id')
        try:
            return NotificationTemplate.objects.get(staff__id=staff_id)
        except NotificationTemplate.DoesNotExist:
            raise NotFound("Notification template does not exist for this staff.")

    @swagger_auto_schema(
        operation_description="Retrieve the notification template for a staff member by staff id.",
        responses={200: NotificationTemplateSerializer()},
        tags = ['notification template']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update the notification template for a staff member by staff id.",
        request_body=NotificationTemplateSerializer,
        responses={200: NotificationTemplateSerializer()},
        tags = ['notification template']
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

# shared logic
class NotificationLogListBase(generics.ListAPIView):
    serializer_class = NotificationLogSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        staff_id = self.kwargs.get('staff_id')
        if staff_id:
            return NotificationLog.objects.filter(staff__id=staff_id)
        return NotificationLog.objects.all()


# All logs 
class NotificationLogListView(NotificationLogListBase):
    swagger_tags = ['notification log']

    @swagger_auto_schema(
        operation_description="Retrieve all notification logs.",
        responses={200: NotificationLogSerializer(many=True)},
        tags=['notification log']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# Logs filtered by staff 
class NotificationLogByStaffListView(NotificationLogListBase):
    swagger_tags = ['notification log']

    @swagger_auto_schema(
        operation_description="Retrieve notification logs for a specific staff member by staff id.",
        manual_parameters=[
            openapi.Parameter(
                'staff_id',
                openapi.IN_PATH,
                description="UUID of the staff member",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: NotificationLogSerializer(many=True)},
        tags=['notification log']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UserForgotPasswordView(APIView):
    swagger_tags = ['auth']
    @swagger_auto_schema(
        request_body=UserForgotPasswordSerializer,
        responses={
            200: openapi.Response(
                description="Password reset link sent.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: "Bad Request"
        },
        tags =  ['auth']
    )
    def post(self, request):
        serializer = UserForgotPasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                data = serializer.save()
                return Response(
                    {"message": "Password reset link sent successfully."},
                    status=status.HTTP_200_OK
                )
            except ValueError as e:
                error_message = str(e)
                if "MS42225" in error_message:
                    return Response(
                        {"message": "You have reached the trial account unique recipients limit."},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY
                    )
                return Response(
                    {"message": "An unexpected error occurred."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserResetPasswordView(APIView):
    """
    Accepts the token, uid, and new password. Resets the password if valid.
    """
    swagger_tags = ['auth']
    @swagger_auto_schema(
        request_body=UserResetPasswordSerializer,
        responses={
            200: openapi.Response(
                description="Password reset successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: "Bad Request"
        },
        tags = ['auth']
    )
    def post(self, request):
        serializer = UserResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # resets the password
            return Response({
                                "message": "Password has been reset successfully."
                            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
