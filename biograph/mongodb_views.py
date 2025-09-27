"""
MongoDB-based views for BiographRenaissance
These views use MongoDB directly for biograph operations
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import logging

from mongodb_client import mongodb_client

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mongodb_biograph_list(request):
    """Get biographs from MongoDB for authenticated user"""
    try:
        # Get user's phone number from Django user
        user_phone = request.user.phone_number
        if not user_phone:
            return Response({
                'error': 'User phone number not found'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Find user in MongoDB
        user = mongodb_client.find_user_by_phone(user_phone)
        if not user:
            return Response({
                'error': 'User not found in MongoDB'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get pagination parameters
        page = int(request.GET.get('page', 1))
        count = int(request.GET.get('count', 20))
        offset = (page - 1) * count
        
        # Get biographs from MongoDB
        biographs = mongodb_client.get_user_biographs(
            str(user['_id']), 
            limit=count, 
            offset=offset
        )
        
        # Format response for iOS app compatibility
        formatted_biographs = []
        for biograph in biographs:
            formatted_biograph = {
                '_id': biograph['_id'],
                'id': biograph['_id'],
                'title': biograph.get('title', ''),
                'biograph_type': biograph.get('biograph_type', '1'),
                'created_date': biograph.get('created_date', '').isoformat() if biograph.get('created_date') else '',
                'updated_date': biograph.get('updated_date', '').isoformat() if biograph.get('updated_date') else '',
                'photo_url': biograph.get('photo_url'),
                'record_url': biograph.get('record_url'),
                'video_url': biograph.get('video_url'),
                'record_text': biograph.get('record_text', ''),
                'record_time': biograph.get('record_time', 0),
                'words_count': biograph.get('words_count', ''),
                'location': biograph.get('location', ''),
                'is_published': biograph.get('is_published', False),
                'is_removed': biograph.get('is_removed', False),
                'status_key': biograph.get('status_key', 1),
                'all_keywords': biograph.get('all_keywords', []),
                'co_authors': biograph.get('co_authors', []),
                'books': biograph.get('books', []),
                'monologues': biograph.get('monologues', {}),
                'last_played_record': biograph.get('last_played_record', ''),
                'last_updated_title': biograph.get('last_updated_title', {}),
                'type': 'biograph'
            }
            formatted_biographs.append(formatted_biograph)
        
        return Response(formatted_biographs)
        
    except Exception as e:
        logger.error(f"Error in mongodb_biograph_list: {e}")
        return Response({
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mongodb_biograph_details(request):
    """Get biograph details from MongoDB"""
    try:
        biograph_id = request.GET.get('biograph_id')
        if not biograph_id:
            return Response({
                'error': 'biograph_id parameter required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get biograph from MongoDB
        biograph = mongodb_client.get_biograph_by_id(biograph_id)
        if not biograph:
            return Response({
                'error': 'Biograph not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Format response for iOS app compatibility
        response_data = {
            'responseData': {
                'Data': {
                    '_id': biograph['_id'],
                    'id': biograph['_id'],
                    'title': biograph.get('title', ''),
                    'biograph_type': biograph.get('biograph_type', '1'),
                    'created_date': biograph.get('created_date', '').isoformat() if biograph.get('created_date') else '',
                    'updated_date': biograph.get('updated_date', '').isoformat() if biograph.get('updated_date') else '',
                    'photo_url': biograph.get('photo_url'),
                    'record_url': biograph.get('record_url'),
                    'video_url': biograph.get('video_url'),
                    'record_text': biograph.get('record_text', ''),
                    'record_time': biograph.get('record_time', 0),
                    'words_count': biograph.get('words_count', ''),
                    'location': biograph.get('location', ''),
                    'is_published': biograph.get('is_published', False),
                    'is_removed': biograph.get('is_removed', False),
                    'status_key': biograph.get('status_key', 1),
                    'all_keywords': biograph.get('all_keywords', []),
                    'co_authors': biograph.get('co_authors', []),
                    'books': biograph.get('books', []),
                    'monologues': biograph.get('monologues', {}),
                    'last_played_record': biograph.get('last_played_record', ''),
                    'last_updated_title': biograph.get('last_updated_title', {}),
                    'type': 'biograph',
                    'records': []  # iOS app expects this field
                }
            }
        }
        
        return Response(response_data)
        
    except Exception as e:
        logger.error(f"Error in mongodb_biograph_details: {e}")
        return Response({
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mongodb_create_biograph(request):
    """Create a new biograph in MongoDB"""
    try:
        # Get user's phone number from Django user
        user_phone = request.user.phone_number
        if not user_phone:
            return Response({
                'error': 'User phone number not found'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Find user in MongoDB
        user = mongodb_client.find_user_by_phone(user_phone)
        if not user:
            return Response({
                'error': 'User not found in MongoDB'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Extract biograph data from request
        biograph_data = {
            'user_id': str(user['_id']),
            'title': request.data.get('title', ''),
            'record_text': request.data.get('record_text', ''),
            'record_time': request.data.get('record_time', 0),
            'words_count': request.data.get('words_count', ''),
            'photo_url': request.data.get('photo_url'),
            'record_url': request.data.get('record_url'),
            'video_url': request.data.get('video_url'),
            'biograph_type': request.data.get('biograph_type', '1'),
            'location': request.data.get('location', ''),
            'all_keywords': request.data.get('all_keywords', []),
            'co_authors': request.data.get('co_authors', []),
            'books': request.data.get('books', []),
            'monologues': request.data.get('monologues', {}),
            'is_published': request.data.get('is_published', False),
            'is_removed': request.data.get('is_removed', False),
            'status_key': request.data.get('status_key', 1),
            'last_played_record': request.data.get('last_played_record', ''),
            'last_updated_title': request.data.get('last_updated_title', {})
        }
        
        # Create biograph in MongoDB
        biograph_id = mongodb_client.create_biograph(biograph_data)
        if not biograph_id:
            return Response({
                'error': 'Failed to create biograph'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'id': biograph_id,
            'message': 'Biograph created successfully'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Error in mongodb_create_biograph: {e}")
        return Response({
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def mongodb_test_connection(request):
    """Test MongoDB connection"""
    try:
        # Test connection
        users_collection = mongodb_client.get_users_collection()
        count = users_collection.count_documents({})
        
        return Response({
            'status': 'connected',
            'database': mongodb_client.db.name,
            'users_count': count
        })
        
    except Exception as e:
        logger.error(f"MongoDB connection test failed: {e}")
        return Response({
            'status': 'error',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
