"""
URL patterns for core app
"""

from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Phone authentication endpoints (compatible with existing BioGraph)
    path('auth/phone/register/', views.phone_register, name='phone_register'),
    path('auth/phone/login/', views.phone_login, name='phone_login'),
    path('auth/phone/verify/', views.phone_verify_otp, name='phone_verify_otp'),
    
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
]
