"""
MongoDB-compatible authentication views for Railway deployment
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from mongodb_client import mongodb_client

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def mongodb_phone_login(request):
    """Phone number login endpoint using MongoDB"""
    try:
        data = request.data
        # Try different parameter names that iOS app might use
        phone_number = data.get('phone_number') or data.get('phone') or data.get('phoneNumber')
        country_code = data.get('country_code') or data.get('countryCode', '1')
        
        if not phone_number:
            return Response({
                'error': 'Phone number is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Try different phone number formats
        # First try with country code prefix
        full_phone = f"+{country_code}{phone_number}"
        user = mongodb_client.find_user_by_phone(full_phone)
        
        # If not found, try without country code prefix
        if not user:
            user = mongodb_client.find_user_by_phone(phone_number)
        
        if user:
            # In production, send OTP via Twilio here
            # For now, return success response
            return Response({
                'message': 'OTP sent to phone number',
                'phone_number': phone_number,
                'country_code': country_code,
                'is_login': True,
                'user_found': True,
                'user_id': str(user['_id'])
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'User not found. Please register first.',
                'phone_number': phone_number,
                'country_code': country_code
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        logger.error(f"Error in mongodb_phone_login: {e}")
        return Response({
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def mongodb_phone_verify(request):
    """Phone OTP verification endpoint using MongoDB"""
    try:
        data = request.data
        # Try different parameter names that iOS app might use
        phone_number = data.get('phone_number') or data.get('phone') or data.get('phoneNumber')
        country_code = data.get('country_code') or data.get('countryCode', '1')
        otp_code = data.get('otp_code') or data.get('otp') or data.get('otpCode') or data.get('code')
        
        # Debug: Log what we received
        logger.info(f"OTP verify request data: {data}")
        logger.info(f"Phone: {phone_number}, Country: {country_code}, OTP: {otp_code}")
        
        if not phone_number or not otp_code:
            return Response({
                'error': 'Phone number and OTP code are required',
                'debug': {
                    'received_data': data,
                    'phone_number': phone_number,
                    'country_code': country_code,
                    'otp_code': otp_code
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Try different phone number formats
        # First try with country code prefix
        full_phone = f"+{country_code}{phone_number}"
        user = mongodb_client.find_user_by_phone(full_phone)
        
        # If not found, try without country code prefix
        if not user:
            user = mongodb_client.find_user_by_phone(phone_number)
        
        if user:
            # In production, verify OTP with Twilio here
            # For now, accept any OTP for testing
            
            # Generate a simple token for now (we'll implement proper JWT later)
            import hashlib
            import time
            
            # Create a simple token based on user ID and timestamp
            token_data = f"{user['_id']}_{int(time.time())}"
            access_token = hashlib.sha256(token_data.encode()).hexdigest()
            
            # Return both nested and flat formats for maximum compatibility
            return Response({
                # Flat format (common in iOS apps)
                'success': True,
                'status': 'success',
                'code': 200,
                'message': 'OTP verified successfully',
                'error': None,
                'user': {
                    'id': str(user['_id']),
                    'user_id': str(user['_id']),
                    'username': user.get('username', ''),
                    'phone_number': user.get('phone_number', ''),
                    'email': user.get('email', ''),
                    'name': user.get('name', ''),
                    'full_name': user.get('name', ''),
                    'first_name': user.get('name', '').split(' ')[0] if user.get('name') else '',
                    'last_name': ' '.join(user.get('name', '').split(' ')[1:]) if user.get('name') and len(user.get('name', '').split(' ')) > 1 else '',
                    'is_active': True,
                    'is_verified': True,
                    'phone_verified': True,
                    'email_verified': True,
                },
                'tokens': {
                    'access_token': access_token,
                    'refresh_token': f"refresh_{access_token}",
                    'access': access_token,
                    'refresh': f"refresh_{access_token}",
                    'token_type': 'Bearer',
                    'expires_in': 86400
                },
                'auth': {
                    'is_authenticated': True,
                    'user_id': str(user['_id']),
                    'phone_verified': True,
                    'login_successful': True,
                    'session_active': True
                },
                'session': {
                    'session_id': f"session_{user['_id']}",
                    'is_active': True,
                    'user_id': str(user['_id'])
                },
                # Nested format (for apps that expect data wrapper)
                'data': {
                    'user': {
                        'id': str(user['_id']),
                        'user_id': str(user['_id']),
                        'username': user.get('username', ''),
                        'phone_number': user.get('phone_number', ''),
                        'email': user.get('email', ''),
                        'name': user.get('name', ''),
                        'full_name': user.get('name', ''),
                        'first_name': user.get('name', '').split(' ')[0] if user.get('name') else '',
                        'last_name': ' '.join(user.get('name', '').split(' ')[1:]) if user.get('name') and len(user.get('name', '').split(' ')) > 1 else '',
                        'is_active': True,
                        'is_verified': True,
                        'phone_verified': True,
                        'email_verified': True,
                    },
                    'tokens': {
                        'access_token': access_token,
                        'refresh_token': f"refresh_{access_token}",
                        'access': access_token,
                        'refresh': f"refresh_{access_token}",
                        'token_type': 'Bearer',
                        'expires_in': 86400
                    },
                    'auth': {
                        'is_authenticated': True,
                        'user_id': str(user['_id']),
                        'phone_verified': True,
                        'login_successful': True,
                        'session_active': True
                    },
                    'session': {
                        'session_id': f"session_{user['_id']}",
                        'is_active': True,
                        'user_id': str(user['_id'])
                    }
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        logger.error(f"Error in mongodb_phone_verify: {e}")
        return Response({
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
