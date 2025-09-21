"""
Views for modern BioGraph API
"""

from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import User, UserProfile, SocialAccount
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    UserProfileSerializer, SocialAccountSerializer, PasswordChangeSerializer,
    PhoneRegistrationSerializer, PhoneOTPSerializer
)

User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """User registration endpoint"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    """User login endpoint"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    """User profile endpoint"""
    user = request.user
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        serializer = UserSerializer(user, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def user_settings(request):
    """User settings endpoint"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'GET':
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """Change password endpoint"""
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def social_accounts(request):
    """Get user's social accounts"""
    accounts = SocialAccount.objects.filter(user=request.user)
    serializer = SocialAccountSerializer(accounts, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_social_account(request, account_id):
    """Delete a social account"""
    account = get_object_or_404(SocialAccount, id=account_id, user=request.user)
    account.delete()
    return Response({'message': 'Social account deleted successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """Get user statistics"""
    user = request.user
    
    stats = {
        'total_biographs': 0,  # Will be implemented when we add biograph models
        'total_friends': 0,     # Will be implemented when we add friend models
        'total_likes': 0,       # Will be implemented when we add like models
        'account_age_days': (user.created_at - user.created_at).days if user.created_at else 0,
        'subscription_status': user.subscription_status,
        'is_verified': user.is_verified,
    }
    
    return Response(stats)


class UserListView(generics.ListAPIView):
    """List users (for search/friends)"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = User.objects.filter(is_active=True)
        
        # Add search functionality
        search = self.request.query_params.get('search', None)
        if search:
            from django.db import models
            queryset = queryset.filter(
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search) |
                models.Q(email__icontains=search)
            )
        
        return queryset.order_by('-created_at')


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def phone_register(request):
    """Phone number registration endpoint (similar to existing BioGraph)"""
    serializer = PhoneRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        # In production, send OTP via Twilio here
        # For now, just return success message
        return Response({
            'message': 'OTP sent to phone number',
            'phone_number': serializer.validated_data['phone_number'],
            'country_code': serializer.validated_data['country_code']
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def phone_verify_otp(request):
    """Verify OTP and complete registration/login"""
    serializer = PhoneOTPSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Phone authentication successful'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def phone_login(request):
    """Phone number login endpoint"""
    serializer = PhoneRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        country_code = serializer.validated_data['country_code']
        
        try:
            # Construct full phone number with country code
            full_phone = f"+{country_code}{phone_number}"
            user = User.objects.get(phone_number=full_phone)
            # In production, send OTP via Twilio here
            return Response({
                'message': 'OTP sent to phone number',
                'phone_number': phone_number,
                'country_code': country_code,
                'is_login': True
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found. Please register first.'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)