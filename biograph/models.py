"""
Biograph models for BiographRenaissance
"""

from django.db import models
from django.utils import timezone
from core.models import User


class BiographModel(models.Model):
    """Biograph content model"""
    
    BIOGRAPH_TYPE = [
        ('1', 'SIMPLE'),
        ('2', 'VIDEO')
    ]
    
    # Core fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='biographs')
    title = models.CharField(max_length=120, default="")
    
    # Content fields
    record_text = models.TextField(null=True, blank=True)
    record_time = models.IntegerField(default=0)
    words_count = models.CharField(max_length=120, null=True, blank=True)
    
    # Media fields
    photo_url = models.URLField(blank=True, null=True)
    record_url = models.URLField(blank=True, null=True)  # Audio file URL
    video_url = models.URLField(blank=True, null=True)  # Video file URL
    
    # Content type
    biograph_type = models.CharField(max_length=1, choices=BIOGRAPH_TYPE, default="1")
    
    # Metadata
    all_keywords = models.JSONField(default=list, blank=True)
    location = models.CharField(max_length=120, default="", null=True, blank=True)
    
    # Social features
    co_authors = models.JSONField(default=list, blank=True)
    books = models.JSONField(default=list, blank=True)
    monologues = models.JSONField(default=dict, blank=True)
    
    # Status fields
    is_published = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)
    status_key = models.IntegerField(default=1)
    
    # Tracking
    last_played_record = models.CharField(max_length=120, default="")
    last_updated_title = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Migration fields
    migrated_from_old_system = models.BooleanField(default=False)
    old_biograph_id = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = 'biographs'
        verbose_name = 'Biograph'
        verbose_name_plural = 'Biographs'
        ordering = ['-created_date']
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"


class CoAuthorModel(models.Model):
    """Co-author relationship model"""
    
    biograph = models.ForeignKey(BiographModel, on_delete=models.CASCADE, related_name='co_author_relationships')
    co_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='co_authored_biographs')
    
    # Status
    is_approved = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)
    
    # Timestamps
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Migration fields
    migrated_from_old_system = models.BooleanField(default=False)
    old_coauthor_id = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = 'co_authors'
        unique_together = ['biograph', 'co_author']
        verbose_name = 'Co-Author'
        verbose_name_plural = 'Co-Authors'
    
    def __str__(self):
        return f"{self.co_author.username} co-authored {self.biograph.title}"


class BookModel(models.Model):
    """Book/Collection model"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=120, default="")
    synopsis = models.CharField(max_length=250, default="", null=True, blank=True)
    
    # Content
    biographs = models.JSONField(default=list, blank=True)
    
    # Status
    is_published = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)
    status_key = models.IntegerField(default=1)
    
    # Timestamps
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Migration fields
    migrated_from_old_system = models.BooleanField(default=False)
    old_book_id = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = 'books'
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['-created_date']
    
    def __str__(self):
        return f"{self.title} by {self.user.username}"


class NotificationModel(models.Model):
    """Notification model"""
    
    NOTIFICATION_TYPE = [
        (1, 'Pending'),
        (2, 'Approved Request'),
        (3, 'Added Co-Author'),
        (4, 'New Record in Biograph'),
        (5, 'Request to publish record'),
        (6, 'Subscribe'),
    ]
    
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPE, default=1)
    biograph = models.ForeignKey(BiographModel, on_delete=models.CASCADE, null=True, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)
    status_key = models.IntegerField(default=1)
    
    # Timestamps
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Migration fields
    migrated_from_old_system = models.BooleanField(default=False)
    old_notification_id = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_date']
    
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}: {self.get_notification_type_display()}"


class RecordedTimeModel(models.Model):
    """Listening time tracking model"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listening_times')
    listening_time = models.IntegerField()
    date_of_listening = models.DateField(default=timezone.now)
    
    # Status
    is_removed = models.BooleanField(default=False)
    status_key = models.IntegerField(default=1)
    
    # Timestamps
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    
    # Migration fields
    migrated_from_old_system = models.BooleanField(default=False)
    old_recorded_time_id = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = 'recorded_times'
        verbose_name = 'Recorded Time'
        verbose_name_plural = 'Recorded Times'
        ordering = ['-date_of_listening']
    
    def __str__(self):
        return f"{self.user.username} listened for {self.listening_time} minutes on {self.date_of_listening}"


class SubscriptionModel(models.Model):
    """Subscription model"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    receipt_id = models.CharField(max_length=200, null=False)
    duration = models.IntegerField()
    product_id = models.CharField(max_length=120, null=False, default="")
    
    # Dates
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    
    # Migration fields
    migrated_from_old_system = models.BooleanField(default=False)
    old_subscription_id = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.user.username} subscription: {self.product_id} ({self.start_date} - {self.end_date})"