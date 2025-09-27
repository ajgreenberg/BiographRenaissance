from rest_framework import serializers
from .models import BiographModel

class BiographSerializer(serializers.ModelSerializer):
    """Serializer for BiographModel"""
    
    class Meta:
        model = BiographModel
        fields = [
            'id', 'title', 'record_text', 'record_time', 'words_count',
            'photo', 'audio', 'video',  # New Railway Volumes fields
            'photo_url', 'record_url', 'video_url',  # Legacy fields
            'biograph_type', 'all_keywords', 'location',
            'co_authors', 'books', 'monologues',
            'is_published', 'is_removed', 'status_key',
            'last_played_record', 'last_updated_title',
            'created_date', 'updated_date'
        ]
        read_only_fields = ['id', 'created_date', 'updated_date']
    
    def to_internal_value(self, data):
        """Map legacy field names to new field names"""
        # Map record_url to audio for iOS app compatibility
        if 'record_url' in data and 'audio' not in data:
            data = data.copy()
            data['audio'] = data.pop('record_url')
        
        return super().to_internal_value(data)
    
    def to_representation(self, instance):
        """Custom representation to include media URLs and iOS compatibility fields"""
        data = super().to_representation(instance)
        
        # Add type field for iOS app compatibility (biographs vs books)
        data['type'] = 'biograph'
        
        # Add _id field for iOS app compatibility (expects _id instead of id)
        data['_id'] = str(instance.id)
        
        # Add media URLs if files exist
        if instance.photo:
            data['photo_url'] = instance.photo.url
        if instance.audio:
            # Primary DRF-style key
            data['audio_url'] = instance.audio.url
            # Backward-compatibility for iOS app expecting 'record_url'
            if not data.get('record_url'):
                data['record_url'] = instance.audio.url
        if instance.video:
            data['video_url'] = instance.video.url
        
        return data
