"""
Health check endpoint for Railway deployment
"""

from django.http import JsonResponse
import os

def health_check(request):
    """Health check endpoint that doesn't require MongoDB"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'BiographRenaissance API',
        'environment': os.getenv('RAILWAY_ENVIRONMENT', 'development'),
        'mongodb_uri_set': bool(os.getenv('MONGODB_URI')),
        'timestamp': '2025-09-27T16:25:00Z'
    })
