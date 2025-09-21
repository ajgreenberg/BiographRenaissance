from django.contrib import admin
from .models import BiographModel, CoAuthorModel, BookModel, NotificationModel, RecordedTimeModel, SubscriptionModel


@admin.register(BiographModel)
class BiographAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'biograph_type', 'is_published', 'created_date']
    list_filter = ['biograph_type', 'is_published', 'is_removed', 'created_date']
    search_fields = ['title', 'user__username', 'record_text']
    readonly_fields = ['created_date', 'updated_date']


@admin.register(CoAuthorModel)
class CoAuthorAdmin(admin.ModelAdmin):
    list_display = ['biograph', 'co_author', 'is_approved', 'created_date']
    list_filter = ['is_approved', 'is_removed', 'created_date']
    search_fields = ['biograph__title', 'co_author__username']


@admin.register(BookModel)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'is_published', 'created_date']
    list_filter = ['is_published', 'is_removed', 'created_date']
    search_fields = ['title', 'user__username', 'synopsis']


@admin.register(NotificationModel)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'notification_type', 'is_read', 'created_date']
    list_filter = ['notification_type', 'is_read', 'is_removed', 'created_date']
    search_fields = ['from_user__username', 'to_user__username']


@admin.register(RecordedTimeModel)
class RecordedTimeAdmin(admin.ModelAdmin):
    list_display = ['user', 'listening_time', 'date_of_listening', 'created_date']
    list_filter = ['date_of_listening', 'created_date']
    search_fields = ['user__username']


@admin.register(SubscriptionModel)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'product_id', 'start_date', 'end_date', 'duration']
    list_filter = ['product_id', 'start_date', 'end_date']
    search_fields = ['user__username', 'receipt_id', 'product_id']