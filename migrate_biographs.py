#!/usr/bin/env python3
"""
Migration script to migrate biograph content from existing BioGraph to BiographRenaissance
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BiographRenaissance.settings')
django.setup()

from core.models import User
from biograph.models import BiographModel, BookModel, NotificationModel, RecordedTimeModel, SubscriptionModel
import pymongo
from datetime import datetime

def migrate_biographs_from_mongodb():
    """Migrate biographs from existing MongoDB to BiographRenaissance"""
    
    print("🔄 Starting biograph migration from existing BioGraph...")
    
    # Connect to existing MongoDB
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["BioGraphDemo"]
        print("✅ Connected to existing MongoDB")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        return
    
    # Migrate biographs
    migrate_biograph_models(db)
    
    # Migrate books
    migrate_book_models(db)
    
    # Migrate notifications
    migrate_notification_models(db)
    
    # Migrate recorded times
    migrate_recorded_time_models(db)
    
    # Migrate subscriptions
    migrate_subscription_models(db)
    
    print("\n🎉 Biograph migration complete!")

def migrate_biograph_models(db):
    """Migrate biograph models"""
    
    print("\n📚 Migrating biographs...")
    
    try:
        old_biographs = db.biographapp_biographmodel.find({})
        count = db.biographapp_biographmodel.count_documents({})
        print(f"Found {count} biographs to migrate")
    except Exception as e:
        print(f"❌ Failed to fetch biographs: {e}")
        return
    
    migrated_count = 0
    error_count = 0
    
    for old_biograph in old_biographs:
        try:
            # Find corresponding user in new system
            old_user_id = str(old_biograph['user_id'])
            new_user = User.objects.filter(old_user_id=old_user_id).first()
            
            if not new_user:
                print(f"⚠️  User not found for biograph {old_biograph.get('title', 'Unknown')}")
                continue
            
            # Check if biograph already exists
            if BiographModel.objects.filter(old_biograph_id=str(old_biograph['_id'])).exists():
                print(f"⏭️  Biograph {old_biograph.get('title', 'Unknown')} already migrated")
                continue
            
            # Create new biograph
            new_biograph = BiographModel.objects.create(
                user=new_user,
                title=old_biograph.get('title', ''),
                record_text=old_biograph.get('record_text', ''),
                record_time=old_biograph.get('record_time', 0),
                words_count=old_biograph.get('words_count', ''),
                photo_url=old_biograph.get('photo_url', ''),
                record_url=old_biograph.get('record_url', ''),
                video_url=old_biograph.get('video_url', ''),
                biograph_type=old_biograph.get('biograph_type', '1'),
                all_keywords=old_biograph.get('allKeywords', []),
                location=old_biograph.get('location', ''),
                co_authors=old_biograph.get('co_authors', []),
                books=old_biograph.get('books', []),
                monologues=old_biograph.get('monologues', {}),
                is_published=old_biograph.get('is_published', False),
                is_removed=old_biograph.get('is_removed', False),
                status_key=old_biograph.get('status_key', 1),
                last_played_record=old_biograph.get('last_played_record', ''),
                last_updated_title=old_biograph.get('last_updated_title', {}),
                created_date=old_biograph.get('created_date', datetime.now()),
                updated_date=old_biograph.get('updated_date', datetime.now()),
                migrated_from_old_system=True,
                old_biograph_id=str(old_biograph['_id']),
            )
            
            migrated_count += 1
            print(f"✅ Migrated biograph: {old_biograph.get('title', 'Unknown')}")
            
        except Exception as e:
            error_count += 1
            print(f"❌ Error migrating biograph {old_biograph.get('title', 'Unknown')}: {e}")
    
    print(f"📊 Biographs: {migrated_count} migrated, {error_count} errors")

def migrate_book_models(db):
    """Migrate book models"""
    
    print("\n📖 Migrating books...")
    
    try:
        old_books = db.authapp_booksmodel.find({})
        count = db.authapp_booksmodel.count_documents({})
        print(f"Found {count} books to migrate")
    except Exception as e:
        print(f"❌ Failed to fetch books: {e}")
        return
    
    migrated_count = 0
    error_count = 0
    
    for old_book in old_books:
        try:
            # Find corresponding user
            old_user_id = str(old_book['user_id'])
            new_user = User.objects.filter(old_user_id=old_user_id).first()
            
            if not new_user:
                print(f"⚠️  User not found for book {old_book.get('title', 'Unknown')}")
                continue
            
            # Check if book already exists
            if BookModel.objects.filter(old_book_id=str(old_book['_id'])).exists():
                print(f"⏭️  Book {old_book.get('title', 'Unknown')} already migrated")
                continue
            
            # Create new book
            new_book = BookModel.objects.create(
                user=new_user,
                title=old_book.get('title', ''),
                synopsis=old_book.get('synopsis', ''),
                biographs=old_book.get('biographs', []),
                is_published=old_book.get('is_published', False),
                is_removed=old_book.get('is_removed', False),
                status_key=old_book.get('status_key', 1),
                created_date=old_book.get('created_date', datetime.now()),
                updated_date=old_book.get('updated_date', datetime.now()),
                migrated_from_old_system=True,
                old_book_id=str(old_book['_id']),
            )
            
            migrated_count += 1
            print(f"✅ Migrated book: {old_book.get('title', 'Unknown')}")
            
        except Exception as e:
            error_count += 1
            print(f"❌ Error migrating book {old_book.get('title', 'Unknown')}: {e}")
    
    print(f"📊 Books: {migrated_count} migrated, {error_count} errors")

def migrate_notification_models(db):
    """Migrate notification models"""
    
    print("\n🔔 Migrating notifications...")
    
    try:
        old_notifications = db.authapp_notifcationmodel.find({})
        count = db.authapp_notifcationmodel.count_documents({})
        print(f"Found {count} notifications to migrate")
    except Exception as e:
        print(f"❌ Failed to fetch notifications: {e}")
        return
    
    migrated_count = 0
    error_count = 0
    
    for old_notification in old_notifications:
        try:
            # Find corresponding users
            from_user = User.objects.filter(old_user_id=str(old_notification['from_id'])).first()
            to_user = User.objects.filter(old_user_id=str(old_notification['to_id'])).first()
            
            if not from_user or not to_user:
                print(f"⚠️  Users not found for notification")
                continue
            
            # Check if notification already exists
            if NotificationModel.objects.filter(old_notification_id=str(old_notification['_id'])).exists():
                continue
            
            # Create new notification
            new_notification = NotificationModel.objects.create(
                from_user=from_user,
                to_user=to_user,
                notification_type=old_notification.get('notification_type', 1),
                is_read=old_notification.get('is_read', False),
                is_removed=old_notification.get('is_removed', False),
                status_key=old_notification.get('status_key', 1),
                created_date=old_notification.get('created_date', datetime.now()),
                updated_date=old_notification.get('updated_date', datetime.now()),
                migrated_from_old_system=True,
                old_notification_id=str(old_notification['_id']),
            )
            
            migrated_count += 1
            
        except Exception as e:
            error_count += 1
            print(f"❌ Error migrating notification: {e}")
    
    print(f"📊 Notifications: {migrated_count} migrated, {error_count} errors")

def migrate_recorded_time_models(db):
    """Migrate recorded time models"""
    
    print("\n⏱️  Migrating recorded times...")
    
    try:
        old_times = db.authapp_recordedtimemodel.find({})
        count = db.authapp_recordedtimemodel.count_documents({})
        print(f"Found {count} recorded times to migrate")
    except Exception as e:
        print(f"❌ Failed to fetch recorded times: {e}")
        return
    
    migrated_count = 0
    error_count = 0
    
    for old_time in old_times:
        try:
            # Find corresponding user
            old_user_id = str(old_time['user_id'])
            new_user = User.objects.filter(old_user_id=old_user_id).first()
            
            if not new_user:
                continue
            
            # Check if recorded time already exists
            if RecordedTimeModel.objects.filter(old_recorded_time_id=str(old_time['_id'])).exists():
                continue
            
            # Create new recorded time
            new_time = RecordedTimeModel.objects.create(
                user=new_user,
                listening_time=old_time.get('listening_time', 0),
                date_of_listening=old_time.get('date_of_listening', datetime.now().date()),
                is_removed=old_time.get('is_removed', False),
                status_key=old_time.get('status_key', 1),
                created_date=old_time.get('created_date', datetime.now()),
                updated_date=old_time.get('updated_date', datetime.now()),
                migrated_from_old_system=True,
                old_recorded_time_id=str(old_time['_id']),
            )
            
            migrated_count += 1
            
        except Exception as e:
            error_count += 1
            print(f"❌ Error migrating recorded time: {e}")
    
    print(f"📊 Recorded Times: {migrated_count} migrated, {error_count} errors")

def migrate_subscription_models(db):
    """Migrate subscription models"""
    
    print("\n💳 Migrating subscriptions...")
    
    try:
        old_subscriptions = db.authapp_subscription.find({})
        count = db.authapp_subscription.count_documents({})
        print(f"Found {count} subscriptions to migrate")
    except Exception as e:
        print(f"❌ Failed to fetch subscriptions: {e}")
        return
    
    migrated_count = 0
    error_count = 0
    
    for old_subscription in old_subscriptions:
        try:
            # Find corresponding user
            old_user_id = str(old_subscription['user_id'])
            new_user = User.objects.filter(old_user_id=old_user_id).first()
            
            if not new_user:
                continue
            
            # Check if subscription already exists
            if SubscriptionModel.objects.filter(old_subscription_id=str(old_subscription['_id'])).exists():
                continue
            
            # Create new subscription
            new_subscription = SubscriptionModel.objects.create(
                user=new_user,
                receipt_id=old_subscription.get('receipt_id', ''),
                duration=old_subscription.get('duration', 0),
                product_id=old_subscription.get('product_id', ''),
                start_date=old_subscription.get('start_date', datetime.now().date()),
                end_date=old_subscription.get('end_date', datetime.now().date()),
                migrated_from_old_system=True,
                old_subscription_id=str(old_subscription['_id']),
            )
            
            migrated_count += 1
            
        except Exception as e:
            error_count += 1
            print(f"❌ Error migrating subscription: {e}")
    
    print(f"📊 Subscriptions: {migrated_count} migrated, {error_count} errors")

def main():
    """Main migration function"""
    print("🚀 BioGraph Content Migration Tool")
    print("=" * 50)
    
    migrate_biographs_from_mongodb()

if __name__ == "__main__":
    main()
