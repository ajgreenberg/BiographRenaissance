"""
URL patterns for core app
"""

from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views, mongodb_auth_views, user_endpoints, simple_auth, complete_auth

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Phone authentication endpoints (compatible with existing BioGraph)
    path('auth/phone/register/', views.phone_register, name='phone_register'),
    path('auth/phone/login/', mongodb_auth_views.mongodb_phone_login, name='phone_login'),
    path('auth/phone/verify/', mongodb_auth_views.mongodb_phone_verify, name='phone_verify_otp'),
    path('auth/phone/verify/simple/', simple_auth.simple_phone_verify, name='simple_phone_verify'),
    path('auth/phone/verify/complete/', complete_auth.complete_phone_verify, name='complete_phone_verify'),
    
    # User profile endpoints
    path('profile/', views.profile, name='profile'),
    path('settings/', views.user_settings, name='user_settings'),
    path('change-password/', views.change_password, name='change_password'),
    path('stats/', views.user_stats, name='user_stats'),
    
    # Social accounts
    path('social-accounts/', views.social_accounts, name='social_accounts'),
    path('social-accounts/<int:account_id>/delete/', views.delete_social_account, name='delete_social_account'),
    
    # User search
    path('users/', views.UserListView.as_view(), name='user_list'),
    
    # User endpoints for iOS app
    path('user/profile/', user_endpoints.user_profile, name='user_profile'),
    path('user/biographs/', user_endpoints.user_biographs, name='user_biographs'),
]
