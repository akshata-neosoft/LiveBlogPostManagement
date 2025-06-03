# user_management/views/login_viewset.py

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from blogpost_management.api_exception import StandardizedException
from user_management.models import Users
from user_management.serializers.user_serializer import UserSerializer
from utils.decorators import trace_log
from utils.helper_methods import (
    hash_string_with_secret_key,
    validate_email,
    validate_password,
)
from utils.permission import IsAuthenticatedWithSimpleToken
from utils.token import create_token
from utils.logger import service_logger
from django.conf import settings


class LoginViewSet(NestedViewSetMixin, ModelViewSet):
    model = Users
    serializer_class = UserSerializer
    queryset = Users.objects.all()

    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        """
        Handle user login and return JWT token if successful.
        """
        try:
            email_id = request.data.get("email_id")
            password = request.data.get("password")

            if not email_id or not password:
                return Response(
                    {"error": True, "message": "Email and password are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = Users.objects.filter(email_id=email_id).first()
            if not user:
                return Response(
                    {"error": True, "message": "No user found with this email"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            hashed_password = hash_string_with_secret_key(
                password, settings.SECRET_KEY_FOR_PASSWORD
            )

            if hashed_password != user.password:
                return Response(
                    {"error": True, "message": "Invalid login credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            token = create_token(user.id, user.email_id)

            return Response(
                {
                    "success": True,
                    "message": "Login successful",
                    "data": {
                        "token": token,
                        "email_id": user.email_id,
                        "user_id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            service_logger.error(f"Login error: {str(e)}")
            return Response(
                {"error": True, "message": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=['post'])
    def sign_up(self, request, *args, **kwargs):
        """
        Register a new user after validating all fields.
        """
        try:
            email_id = request.data.get("email_id")
            password = request.data.get("password")
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")

            # Basic validation
            if not email_id:
                return Response(
                    {"error": True, "message": "Email is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not validate_email(email_id):
                return Response(
                    {"error": True, "message": "Invalid email format"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if Users.objects.filter(email_id=email_id).exists():
                return Response(
                    {"error": True, "message": "Email is already registered"},
                    status=status.HTTP_409_CONFLICT,
                )
            if not password or not validate_password(password):
                return Response(
                    {
                        "error": True,
                        "message": "Password must contain a special character, number, and start with a capital letter",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not first_name or not last_name:
                return Response(
                    {
                        "error": True,
                        "message": "First name and last name are required",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create user
            hashed_password = hash_string_with_secret_key(
                password, settings.SECRET_KEY_FOR_PASSWORD
            )
            user_data = {
                "email_id": email_id,
                "password": hashed_password,
                "first_name": first_name,
                "last_name": last_name,
            }

            serializer = self.serializer_class(data=user_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {"success": True, "message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            service_logger.error(f"Sign-up error: {str(e)}")
            return Response(
                {"error": True, "message": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class ProfileViewSet(NestedViewSetMixin, ModelViewSet):
    model = Users
    serializer_class = UserSerializer
    queryset = Users.objects.all()
    permission_classes = [IsAuthenticatedWithSimpleToken]

    @trace_log
    def update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = False
            obj = self.get_object()
            serializer = self.serializer_class(obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = self.serializer_class(obj).data
            return Response({"Success": True, "message": "Blog Post Updated Successfully",
                             "data": response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            service_logger.error(str(e))
            raise StandardizedException(error_status=True,
                                        error_obj=e,
                                        status_code=status.HTTP_400_BAD_REQUEST)
