"""
Custom authentication classes for MongoDB compatibility
"""

from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import AnonymousUser


class FlexibleJWTAuthentication(BaseAuthentication):
    """
    Custom authentication that allows both JWT tokens and simple tokens
    Falls back to AnonymousUser if token validation fails
    """
    
    def authenticate(self, request):
        # Try JWT authentication first
        jwt_auth = JWTAuthentication()
        try:
            user, token = jwt_auth.authenticate(request)
            if user:
                return (user, token)
        except:
            pass
        
        # If JWT fails, check for simple token in Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            # For simple tokens, return AnonymousUser
            # This allows AllowAny endpoints to work
            return (AnonymousUser(), token)
        
        return None
    
    def authenticate_header(self, request):
        return 'Bearer'


class NoAuthAuthentication(BaseAuthentication):
    """
    Authentication class that never authenticates
    Always returns AnonymousUser for AllowAny endpoints
    """
    
    def authenticate(self, request):
        # Always return AnonymousUser
        return (AnonymousUser(), None)
    
    def authenticate_header(self, request):
        return 'Bearer'
