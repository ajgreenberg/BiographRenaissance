"""
MongoDB-based views for BiographRenaissance using migrated data structure
These views use the actual migrated collections: AuthApp_usermodel and biographApp_biographmodel
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
@permission_classes([AllowAny])
def mongodb_biograph_list_migrated(request):
    """Get biographs from migrated MongoDB collections for authenticated user"""
    try:
        # For now, use a default user (AJ Greenberg) since we're testing
        # In production, we'll need to implement proper token-based authentication
        user_phone = "8479873207"  # AJ Greenberg's phone number
        
        # Find user in migrated AuthApp_usermodel collection
        user = mongodb_client.find_user_by_phone(user_phone)
        if not user:
            return Response({
                'error': 'User not found in migrated data'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get pagination parameters
        page = int(request.GET.get('page', 1))
        count = int(request.GET.get('count', 20))
        offset = (page - 1) * count
        
        # Get both owned and co-authored biographs
        owned_biographs = mongodb_client.get_user_biographs(
            str(user['_id']), 
            limit=count, 
            offset=offset
        )
        
        # Also get co-authored biographs
        co_authored_biographs = mongodb_client.get_co_authored_biographs(
            user.get('old_user_id', ''), 
            limit=count, 
            offset=offset
        )
        
        # Combine and deduplicate biographs
        all_biographs = owned_biographs + co_authored_biographs
        # Remove duplicates based on _id
        seen_ids = set()
        unique_biographs = []
        for bg in all_biographs:
            if bg['_id'] not in seen_ids:
                seen_ids.add(bg['_id'])
                unique_biographs.append(bg)
        
        # Sort by created_date descending
        biographs = sorted(unique_biographs, key=lambda x: x.get('created_date', ''), reverse=True)[:count]
        
        # Format response for iOS app compatibility using migrated field names
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
                'all_keywords': biograph.get('allKeywords', []),  # Note: migrated data uses 'allKeywords'
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
        logger.error(f"Error in mongodb_biograph_list_migrated: {e}")
        return Response({
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mongodb_biograph_details_migrated(request):
    """Get biograph details from migrated MongoDB collections"""
    try:
        biograph_id = request.GET.get('biograph_id')
        if not biograph_id:
            return Response({
                'error': 'biograph_id parameter required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get biograph from migrated biographApp_biographmodel collection
        biograph = mongodb_client.get_biograph_by_id(biograph_id)
        if not biograph:
            return Response({
                'error': 'Biograph not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Format response for iOS app compatibility using migrated field names
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
                    'all_keywords': biograph.get('allKeywords', []),  # Note: migrated data uses 'allKeywords'
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
        logger.error(f"Error in mongodb_biograph_details_migrated: {e}")
        return Response({
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def mongodb_test_connection_migrated(request):
    """Test MongoDB connection with migrated collections"""
    try:
        # Test connection
        users_collection = mongodb_client.get_users_collection()
        biographs_collection = mongodb_client.get_biographs_collection()
        
        users_count = users_collection.count_documents({})
        biographs_count = biographs_collection.count_documents({})
        
        return Response({
            'status': 'connected',
            'database': mongodb_client.db.name,
            'users_count': users_count,
            'biographs_count': biographs_count,
            'collections': {
                'users': 'AuthApp_usermodel',
                'biographs': 'biographApp_biographmodel'
            }
        })
        
    except Exception as e:
        logger.error(f"MongoDB connection test failed: {e}")
        return Response({
            'status': 'error',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def mongodb_find_user_by_phone(request):
    """Find user by phone number in migrated data"""
    try:
        phone_number = request.GET.get('phone')
        if not phone_number:
            return Response({
                'error': 'phone parameter required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = mongodb_client.find_user_by_phone(phone_number)
        if user:
            return Response({
                'found': True,
                'user': {
                    'id': str(user['_id']),
                    'username': user.get('username', ''),
                    'phone_number': user.get('phone_number', ''),
                    'email': user.get('email', ''),
                    'name': user.get('name', '')
                }
            })
        else:
            return Response({
                'found': False,
                'message': f'User with phone {phone_number} not found'
            })
        
    except Exception as e:
        logger.error(f"Error finding user by phone: {e}")
        return Response({
            'error': 'Internal server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
