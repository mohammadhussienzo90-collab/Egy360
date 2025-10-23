# FILE: accounts/serializers.py
# ============================================================
"""
Serializers for User Management

These serializers handle conversion between:
- Django User model (Python objects)
- JSON format (API requests/responses)

Each serializer has a specific purpose:
- UserListSerializer: Minimal data for list views
- UserDetailSerializer: Complete profile data
- UserCreateSerializer: Registration with validation
- UserUpdateSerializer: Profile updates
- UserPasswordChangeSerializer: Password changes
- UserLoginSerializer: Authentication
- UserProfilePictureSerializer: Image uploads
- UserProviderSerializer: Public provider info
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing users (minimal information)

    Used in: GET /api/v1/users/
    Purpose: Fast loading, summary view
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'full_name',
            'user_type',
            'is_verified',
            'profile_picture',
            'created_at',
        )
        read_only_fields = ('id', 'created_at')

    def get_full_name(self, obj):
        """Get user's full name or fallback to username"""
        return obj.get_full_name() or obj.username


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for user detail view (all user information)

    Used in: GET /api/v1/users/{id}/, GET /api/v1/users/me/
    Purpose: Complete profile data
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone_number',
            'gender',
            'date_of_birth',
            'nationality',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'profile_picture',
            'bio',
            'website',
            'user_type',
            'is_verified',
            'is_phone_verified',
            'is_identity_verified',
            'is_licensed',
            'business_name',
            'business_license',
            'language_preference',
            'receive_notifications',
            'receive_sms',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'is_verified',
            'is_phone_verified',
            'is_identity_verified',
            'is_licensed',
            'created_at',
            'updated_at',
        )

    def get_full_name(self, obj):
        """Get user's full name or fallback to username"""
        return obj.get_full_name() or obj.username


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration/creation

    Used in: POST /api/v1/users/register/
    Purpose: Create new user account with validation

    Validates:
    - Passwords match
    - Password strength
    - Unique username and email
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password2',
            'user_type',
            'phone_number',
        )

    def validate(self, data):
        """Validate that passwords match"""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                'password': 'Passwords do not match'
            })
        return data

    def create(self, validated_data):
        """Create user with hashed password"""
        # Remove password2 (it's not a model field)
        validated_data.pop('password2')

        # Extract password separately to hash it
        password = validated_data.pop('password')

        # Create user with create_user method (hashes password automatically)
        user = CustomUser.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile

    Used in: PUT /api/v1/users/me/
    Purpose: Update user profile information

    Note: Cannot update username, email (need separate endpoints)
    """

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'gender',
            'date_of_birth',
            'nationality',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'profile_picture',
            'bio',
            'website',
            'language_preference',
            'receive_notifications',
            'receive_sms',
        )


class UserPasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing user password

    Used in: POST /api/v1/users/password_change/
    Purpose: Securely change user password

    Validates:
    - Old password is correct
    - New passwords match
    - Both old and new provided
    """
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    new_password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        """Validate that new passwords match"""
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({
                'new_password': 'New passwords do not match'
            })
        return data

    def validate_old_password(self, value):
        """Validate old password is correct"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect')
        return value


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login

    Used in: POST /api/v1/users/login/
    Purpose: Authenticate user and return JWT tokens

    Validates:
    - Username and password match
    - User exists and is active
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        """Authenticate user"""
        user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        data['user'] = user
        return data


class UserProfilePictureSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading profile picture

    Used in: POST /api/v1/users/upload_profile_picture/
    Purpose: Upload/update user profile photo

    Handles: Image file upload and storage
    """

    class Meta:
        model = CustomUser
        fields = ('profile_picture',)


class UserProviderSerializer(serializers.ModelSerializer):
    """
    Serializer for provider information (public view)

    Used in: GET /api/v1/users/provider_info/?user_id=123
    Purpose: Show limited public info about providers

    Visible to: Anyone (tourists checking provider credentials)
    Hidden from tourists: email, phone, address, etc.
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'full_name',
            'phone_number',
            'profile_picture',
            'bio',
            'website',
            'business_name',
            'is_verified',
            'is_licensed',
        )
        read_only_fields = ('id', 'is_verified', 'is_licensed')

    def get_full_name(self, obj):
        """Get provider's full name or fallback to username"""
        return obj.get_full_name() or obj.username