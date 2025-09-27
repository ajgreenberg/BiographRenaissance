"""
Debug MongoDB connection for Railway
"""

from django.http import JsonResponse
import os
import pymongo
from pymongo import MongoClient

def debug_mongodb(request):
    """Debug MongoDB connection details"""
    try:
        mongodb_uri = os.getenv('MONGODB_URI', 'NOT_SET')
        
        # Test connection
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        db = client.get_default_database()
        db.command('ping')
        
        return JsonResponse({
            'status': 'success',
            'mongodb_uri_set': bool(os.getenv('MONGODB_URI')),
            'mongodb_uri_length': len(mongodb_uri) if mongodb_uri != 'NOT_SET' else 0,
            'connection_test': 'success',
            'database_name': db.name,
            'environment': os.getenv('RAILWAY_ENVIRONMENT', 'development')
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'mongodb_uri_set': bool(os.getenv('MONGODB_URI')),
            'mongodb_uri_length': len(os.getenv('MONGODB_URI', '')) if os.getenv('MONGODB_URI') else 0,
            'connection_test': 'failed',
            'error': str(e),
            'environment': os.getenv('RAILWAY_ENVIRONMENT', 'development')
        })
