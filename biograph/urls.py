"""
URL patterns for biograph app
"""

from django.urls import path
from . import mongodb_views, mongodb_views_migrated, simple_test, health_check

urlpatterns = [
    # Health check endpoint (no MongoDB required)
    path('health/', health_check.health_check, name='health-check'),
    
    # Simple test endpoint (no MongoDB required)
    path('simple-test/', simple_test.simple_test, name='simple-test'),
    
    # MongoDB-based views (new)
    path('mongodb/', mongodb_views.mongodb_biograph_list, name='mongodb-biograph-list'),
    path('mongodb/details/', mongodb_views.mongodb_biograph_details, name='mongodb-biograph-details'),
    path('mongodb/create/', mongodb_views.mongodb_create_biograph, name='mongodb-create-biograph'),
    path('mongodb/test/', mongodb_views.mongodb_test_connection, name='mongodb-test-connection'),
    
    # MongoDB-based views using migrated data structure
    path('migrated/', mongodb_views_migrated.mongodb_biograph_list_migrated, name='mongodb-biograph-list-migrated'),
    path('migrated/details/', mongodb_views_migrated.mongodb_biograph_details_migrated, name='mongodb-biograph-details-migrated'),
    path('migrated/test/', mongodb_views_migrated.mongodb_test_connection_migrated, name='mongodb-test-connection-migrated'),
    path('migrated/find-user/', mongodb_views_migrated.mongodb_find_user_by_phone, name='mongodb-find-user-by-phone'),
]