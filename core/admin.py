"""
Admin configuration for modern BioGraph models
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, SocialAccount


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom user admin with modern fields"""
    
    list_display = ('email', 'first_name', 'last_name', 'is_verified', 'subscription_status', 'is_active', 'created_at')
    list_filter = ('is_verified', 'subscription_status', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'bio', 'profile_picture', 'date_of_birth')}),
        ('Social Authentication', {'fields': ('google_id', 'apple_id')}),
        ('App Settings', {'fields': ('is_verified', 'subscription_status')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """User profile admin"""
    
    list_display = ('user', 'profile_visibility', 'email_notifications', 'push_notifications', 'theme', 'created_at')
    list_filter = ('profile_visibility', 'email_notifications', 'push_notifications', 'sms_notifications', 'theme', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Privacy Settings', {'fields': ('profile_visibility',)}),
        ('Notifications', {'fields': ('email_notifications', 'push_notifications', 'sms_notifications')}),
        ('Preferences', {'fields': ('theme',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    """Social account admin"""
    
    list_display = ('user', 'provider', 'provider_email', 'created_at')
    list_filter = ('provider', 'created_at')
    search_fields = ('user__email', 'provider_email', 'provider_id')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Account Info', {'fields': ('user', 'provider', 'provider_id', 'provider_email')}),
        ('Provider Data', {'fields': ('provider_data',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )