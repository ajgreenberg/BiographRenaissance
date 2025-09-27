"""
Minimal Django app for Railway deployment testing
"""

from django.http import JsonResponse
import os

def minimal_health(request):
    """Minimal health check that doesn't import any MongoDB modules"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Minimal Django app is running',
        'environment': os.getenv('RAILWAY_ENVIRONMENT', 'development'),
        'port': os.getenv('PORT', '8000'),
        'mongodb_uri_set': bool(os.getenv('MONGODB_URI')),
    })
