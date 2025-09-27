"""
Simple test view that doesn't require MongoDB
"""

from django.http import JsonResponse

def simple_test(request):
    """Simple test endpoint that doesn't require MongoDB"""
    return JsonResponse({
        'status': 'success',
        'message': 'Django app is running',
        'timestamp': '2025-09-27T16:20:00Z'
    })
