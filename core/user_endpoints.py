"""
User-related endpoints for iOS app compatibility
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import logging
from mongodb_client import mongodb_client

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_profile(request):
    """Get user profile data"""
    try:
        # For now, return AJ Greenberg's profile
        user_phone = "8479873207"
        user = mongodb_client.find_user_by_phone(user_phone)
        
        if user:
            return Response({
                'success': True,
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
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        logger.error(f"Error in user_profile: {e}")
        return Response({
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_biographs(request):
    """Get user's biographs"""
    try:
        # For now, return AJ Greenberg's biographs
        user_phone = "8479873207"
        user = mongodb_client.find_user_by_phone(user_phone)
        
        if user:
            # Get biographs for this user using the same logic as the working endpoint
            # Use the old_user_id approach
            old_user_id = user.get('old_user_id')
            if old_user_id:
                biographs = mongodb_client.get_user_biographs_by_old_id(old_user_id, limit=10)
            else:
                biographs = []
            
            return Response({
                'success': True,
                'biographs': biographs,
                'count': len(biographs),
                'user_id': str(user['_id']),
                'old_user_id': old_user_id
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        logger.error(f"Error in user_biographs: {e}")
        return Response({
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
