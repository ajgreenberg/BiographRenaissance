"""
Modern User Models for BioGraph
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Modern user model with social authentication support"""
    
    # Basic profile info
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)  # Make nullable for phone-only users
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    country_code = models.CharField(max_length=5, default="1")
    is_phone_verified = models.BooleanField(default=False)
    
    # Migration fields
    migrated_from_old_system = models.BooleanField(default=False)
    old_user_id = models.CharField(max_length=100, null=True, blank=True)
    
    # Profile details
    bio = models.TextField(blank=True)
    profile_picture = models.URLField(blank=True)  # Cloudinary URL
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Social authentication
    google_id = models.CharField(max_length=100, blank=True)
    apple_id = models.CharField(max_length=100, blank=True)
    
    # App-specific fields
    is_verified = models.BooleanField(default=False)
    subscription_status = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('premium', 'Premium'),
            ('pro', 'Pro'),
        ],
        default='free'
    )
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # Settings
    USERNAME_FIELD = 'email'  # Primary login field
    REQUIRED_FIELDS = ['username']
    
    def get_login_field(self):
        """Return the field used for login (email or phone)"""
        return self.email if self.email else f"+{self.country_code}{self.phone_number}"
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.email} ({self.get_full_name()})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username


class UserProfile(models.Model):
    """Extended user profile information"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Privacy settings
    profile_visibility = models.CharField(
        max_length=20,
        choices=[
            ('public', 'Public'),
            ('friends', 'Friends Only'),
            ('private', 'Private'),
        ],
        default='public'
    )
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    
    # App preferences
    theme = models.CharField(
        max_length=20,
        choices=[
            ('light', 'Light'),
            ('dark', 'Dark'),
            ('auto', 'Auto'),
        ],
        default='auto'
    )
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"Profile for {self.user.email}"


class SocialAccount(models.Model):
    """Social authentication accounts"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_accounts')
    
    provider = models.CharField(
        max_length=20,
        choices=[
            ('google', 'Google'),
            ('apple', 'Apple'),
            ('facebook', 'Facebook'),
        ]
    )
    
    provider_id = models.CharField(max_length=100)
    provider_email = models.EmailField()
    
    # Additional provider data
    provider_data = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'social_accounts'
        unique_together = ['provider', 'provider_id']
        verbose_name = 'Social Account'
        verbose_name_plural = 'Social Accounts'
    
    def __str__(self):
        return f"{self.user.email} - {self.provider}"