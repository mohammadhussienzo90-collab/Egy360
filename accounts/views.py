# FILE: accounts/views.py
# ============================================================
"""
Views for Accounts App

This file contains the UserViewSet which handles:
- User registration (signup)
- User login (authentication)
- Profile viewing and updating
- Password changes
- Profile picture uploads
- Provider information viewing
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import CustomUser
from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserPasswordChangeSerializer,
    UserLoginSerializer,
    UserProfilePictureSerializer,
    UserProviderSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users

    Handles:
    - User registration
    - User login with JWT tokens
    - Profile viewing and editing
    - Password management
    - Profile picture uploads
    - Provider information viewing

    Endpoints created:
    - POST /api/v1/accounts/users/register/ → Create new user
    - POST /api/v1/accounts/users/login/ → Authenticate and get tokens
    - GET /api/v1/accounts/users/me/ → Get current user profile
    - PUT /api/v1/accounts/users/me/ → Update current user
    - POST /api/v1/accounts/users/password_change/ → Change password
    - POST /api/v1/accounts/users/upload_profile_picture/ → Upload photo
    - GET /api/v1/accounts/users/provider_info/?user_id=123 → Get provider info
    - Standard CRUD: GET /users/, POST /users/, GET /users/{id}/, etc.
    """

    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action

        Different actions need different serializers:
        - list: minimal data (fast)
        - retrieve: complete data (detailed)
        - create/register: validation for new users
        - update: only editable fields
        - login: authentication
        """
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action in ['create', 'register']:
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update', 'update_profile']:
            return UserUpdateSerializer
        elif self.action == 'password_change':
            return UserPasswordChangeSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        elif self.action == 'upload_profile_picture':
            return UserProfilePictureSerializer
        elif self.action == 'provider_info':
            return UserProviderSerializer
        return UserDetailSerializer

    def get_permissions(self):
        """
        Set permissions based on action

        Permission rules:
        - register & login: anyone (AllowAny)
        - me, update_profile, password_change: logged in user (IsAuthenticated)
        - other actions: logged in user OR read-only (IsAuthenticatedOrReadOnly)
        """
        if self.action in ['register', 'login']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['me', 'update_profile', 'password_change', 'upload_profile_picture']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]

        return [permission() for permission in permission_classes]

    # ================================================================
    # AUTHENTICATION ENDPOINTS
    # ================================================================

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """
        Register a new user

        POST /api/v1/accounts/users/register/

        Request body:
        {
            "username": "ali_cairo",
            "email": "ali@example.com",
            "password": "SecurePass123!",
            "password2": "SecurePass123!",
            "user_type": "tourist",
            "first_name": "Ali",
            "last_name": "Mohammed",
            "phone_number": "+201001234567"
        }

        Response:
        {
            "id": 1,
            "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "user": {
                "id": 1,
                "username": "ali_cairo",
                "email": "ali@example.com",
                ...
            },
            "message": "Registration successful!"
        }
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Create the user
            user = serializer.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    'id': user.id,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserDetailSerializer(user).data,
                    'message': 'Registration successful!'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """
        Login user and get JWT tokens

        POST /api/v1/accounts/users/login/

        Request body:
        {
            "username": "ali_cairo",
            "password": "SecurePass123!"
        }

        Response:
        {
            "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "user": {...},
            "message": "Login successful!"
        }

        Frontend Usage:
        - Store access token (use for requests)
        - Store refresh token (get new access when expired)
        - Include token: Authorization: Bearer {access_token}
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate JWT tokens for this user
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserDetailSerializer(user).data,
                    'message': 'Login successful!'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # ================================================================
    # PROFILE ENDPOINTS
    # ================================================================

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Get current user's profile

        GET /api/v1/accounts/users/me/
        Headers: Authorization: Bearer {access_token}

        Response:
        {
            "id": 1,
            "username": "ali_cairo",
            "email": "ali@example.com",
            "first_name": "Ali",
            "last_name": "Mohammed",
            ...complete profile data...
        }
        """
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        """
        Update current user's profile

        PUT /api/v1/accounts/users/me/
        Headers: Authorization: Bearer {access_token}

        Request body (any combination of fields):
        {
            "first_name": "Ali",
            "phone_number": "+201001234567",
            "bio": "Love traveling Egypt!",
            "language_preference": "ar"
        }

        Response:
        {
            "message": "Profile updated successfully!",
            "user": {...updated profile...}
        }
        """
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Profile updated successfully!',
                    'user': UserDetailSerializer(request.user).data
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================================================================
    # SECURITY ENDPOINTS
    # ================================================================

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def password_change(self, request):
        """
        Change user password

        POST /api/v1/accounts/users/password_change/
        Headers: Authorization: Bearer {access_token}

        Request body:
        {
            "old_password": "OldPass123!",
            "new_password": "NewPass456!",
            "new_password2": "NewPass456!"
        }

        Response:
        {
            "message": "Password changed successfully!"
        }
        """
        serializer = UserPasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response(
                {'message': 'Password changed successfully!'},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def upload_profile_picture(self, request):
        """
        Upload user's profile picture

        POST /api/v1/accounts/users/upload_profile_picture/
        Headers: Authorization: Bearer {access_token}
        Body: multipart/form-data with 'profile_picture' file

        Response:
        {
            "profile_picture": "https://egy360.com/media/profiles/user_1.jpg",
            "message": "Profile picture uploaded!"
        }
        """
        serializer = UserProfilePictureSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'profile_picture': request.user.profile_picture.url if request.user.profile_picture else None,
                    'message': 'Profile picture uploaded!'
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================================================================
    # PROVIDER INFO ENDPOINT
    # ================================================================

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def provider_info(self, request):
        """
        Get public information about a provider

        GET /api/v1/accounts/users/provider_info/?user_id=123

        Used by: Tourists checking provider credentials
        Returns: Limited public profile info only

        Response:
        {
            "id": 123,
            "username": "hotel_cairo",
            "first_name": "Cairo",
            "last_name": "Hotels",
            "profile_picture": "https://...",
            "bio": "5-star luxury hotels",
            "business_name": "Cairo Luxury Hotels",
            "is_verified": true,
            "is_licensed": true
        }
        """
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response(
                {'error': 'user_id parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = CustomUser.objects.get(id=user_id, user_type='provider')
            serializer = UserProviderSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'Provider not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    # ================================================================
    # STANDARD CRUD - DESTROY (DELETE)
    # ================================================================

    def destroy(self, request, *args, **kwargs):
        """
        Delete user account

        DELETE /api/v1/accounts/users/{id}/
        Headers: Authorization: Bearer {access_token}

        Rules:
        - User can only delete their own account
        - Admin can delete any account
        """
        user = self.get_object()

        # Check permission: user can delete own account or admin can delete any
        if request.user != user and not request.user.is_staff:
            return Response(
                {'error': 'You can only delete your own account'},
                status=status.HTTP_403_FORBIDDEN
            )

        user.delete()
        return Response(
            {'message': 'Account deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )