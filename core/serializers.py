"""
Serializers for modern BioGraph API
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserProfile, SocialAccount


class UserSerializer(serializers.ModelSerializer):
    """User serializer for API responses"""
    
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'bio', 'profile_picture', 'date_of_birth',
            'is_verified', 'subscription_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_verified']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'phone_number', 'country_code',
            'password', 'password_confirm'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        # Create username from email or phone
        if validated_data.get('email'):
            validated_data['username'] = validated_data['email']
        else:
            validated_data['username'] = f"+{validated_data.get('country_code', '1')}{validated_data['phone_number']}"
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """User login serializer"""
    
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password')


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer"""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'profile_visibility', 'email_notifications',
            'push_notifications', 'sms_notifications', 'theme',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class SocialAccountSerializer(serializers.ModelSerializer):
    """Social account serializer"""
    
    class Meta:
        model = SocialAccount
        fields = [
            'id', 'provider', 'provider_id', 'provider_email',
            'provider_data', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PasswordChangeSerializer(serializers.Serializer):
    """Password change serializer"""
    
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect')
        return value


class PhoneRegistrationSerializer(serializers.Serializer):
    """Phone number registration serializer"""
    
    phone_number = serializers.CharField(max_length=20)
    country_code = serializers.CharField(max_length=5, default="1")
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    
    def validate_phone_number(self, value):
        # Check if phone number already exists
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('Phone number already registered')
        return value


class PhoneOTPSerializer(serializers.Serializer):
    """Phone OTP verification serializer"""
    
    phone_number = serializers.CharField(max_length=20)
    country_code = serializers.CharField(max_length=5, default="1")
    otp = serializers.CharField(max_length=6)
    is_login = serializers.BooleanField(default=False)
    
    def validate(self, attrs):
        phone_number = attrs['phone_number']
        country_code = attrs['country_code']
        otp = attrs['otp']
        is_login = attrs['is_login']
        
        # For testing purposes, accept OTP "123456"
        if otp == "123456":
            if is_login:
                try:
                    # Construct full phone number with country code
                    full_phone = f"+{country_code}{phone_number}"
                    user = User.objects.get(phone_number=full_phone)
                    attrs['user'] = user
                    return attrs
                except User.DoesNotExist:
                    raise serializers.ValidationError('User not found')
            else:
                # Create new user for registration
                username = f"+{country_code}{phone_number}"
                full_phone = f"+{country_code}{phone_number}"
                user = User.objects.create(
                    username=username,
                    phone_number=full_phone,
                    country_code=country_code,
                    is_phone_verified=True
                )
                UserProfile.objects.create(user=user)
                attrs['user'] = user
                return attrs
        
        # In production, verify OTP with Twilio here
        # For now, raise validation error for other OTPs
        raise serializers.ValidationError('Invalid OTP')

