#!/usr/bin/env python3
"""
Migration script to migrate users from existing BioGraph to BiographRenaissance
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BiographRenaissance.settings')
django.setup()

from core.models import User, UserProfile
import pymongo
from datetime import datetime

def migrate_users_from_mongodb():
    """Migrate users from existing MongoDB to BiographRenaissance"""
    
    print("🔄 Starting user migration from existing BioGraph...")
    
    # Connect to existing MongoDB (update connection string)
    try:
        # For local MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["BioGraphDemo"]
        
        # For MongoDB Atlas, use:
        # client = pymongo.MongoClient("mongodb+srv://username:password@cluster.mongodb.net/BioGraphDemo")
        # db = client["BioGraphDemo"]
        
        print("✅ Connected to existing MongoDB")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        return
    
    # Get existing users
    try:
        old_users = db.authapp_usermodel.find({})
        user_count = db.authapp_usermodel.count_documents({})
        print(f"📊 Found {user_count} users to migrate")
    except Exception as e:
        print(f"❌ Failed to fetch users: {e}")
        return
    
    migrated_count = 0
    skipped_count = 0
    error_count = 0
    
    for old_user in old_users:
        try:
            # Check if user already exists
            if User.objects.filter(old_user_id=str(old_user['_id'])).exists():
                print(f"⏭️  Skipping user {old_user['username']} - already migrated")
                skipped_count += 1
                continue
            
            # Create new user
            username = old_user['username']
            phone_number = old_user['phone_number']
            country_code = str(old_user.get('country_code', '1'))
            
            # Create username for new system
            new_username = f"+{country_code}{phone_number}"
            
            new_user = User.objects.create(
                username=new_username,
                phone_number=phone_number,
                country_code=country_code,
                first_name=old_user.get('name', ''),
                profile_picture=old_user.get('profile_pic_url', ''),
                migrated_from_old_system=True,
                old_user_id=str(old_user['_id']),
                is_phone_verified=True,  # Assume verified in old system
                is_premium_member=old_user.get('is_premium_member', False),
                created_at=old_user.get('created_time', datetime.now()),
                updated_at=old_user.get('updated_time', datetime.now()),
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=new_user,
                profile_visibility=map_privacy_setting(old_user.get('profile_settings', 'F')),
                email_notifications=old_user.get('email_notification', {}).get('all', True),
                push_notifications=old_user.get('push_notification', {}).get('all', True),
            )
            
            migrated_count += 1
            print(f"✅ Migrated user: {username} -> {new_username}")
            
        except Exception as e:
            error_count += 1
            print(f"❌ Error migrating user {old_user.get('username', 'unknown')}: {e}")
    
    print("\n📊 Migration Summary:")
    print(f"✅ Successfully migrated: {migrated_count}")
    print(f"⏭️  Skipped (already exists): {skipped_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📈 Total processed: {migrated_count + skipped_count + error_count}")


def map_privacy_setting(old_setting):
    """Map old privacy settings to new ones"""
    mapping = {
        'P': 'public',    # PUBLIC
        'F': 'friends',   # FRIENDS
        'O': 'private',   # ONLY_ME
    }
    return mapping.get(old_setting, 'friends')


def test_phone_authentication():
    """Test phone authentication with migrated users"""
    print("\n🧪 Testing phone authentication...")
    
    # Get a migrated user
    migrated_user = User.objects.filter(migrated_from_old_system=True).first()
    
    if migrated_user:
        print(f"📱 Testing with user: {migrated_user.phone_number}")
        print(f"🔑 Username: {migrated_user.username}")
        print(f"✅ Phone verified: {migrated_user.is_phone_verified}")
        print(f"📅 Created: {migrated_user.created_at}")
        print(f"🆔 Old user ID: {migrated_user.old_user_id}")
    else:
        print("❌ No migrated users found")


def create_test_phone_user():
    """Create a test user with phone authentication"""
    print("\n🧪 Creating test phone user...")
    
    test_phone = "1234567890"
    test_country_code = "1"
    
    # Check if test user exists
    if User.objects.filter(phone_number=test_phone).exists():
        print(f"⏭️  Test user with phone {test_phone} already exists")
        return
    
    # Create test user
    username = f"+{test_country_code}{test_phone}"
    user = User.objects.create_user(
        username=username,
        phone_number=test_phone,
        country_code=test_country_code,
        first_name="Test",
        last_name="User",
        is_phone_verified=True
    )
    
    # Create profile
    UserProfile.objects.create(user=user)
    
    print(f"✅ Created test user: {username}")
    print(f"📱 Phone: +{test_country_code}{test_phone}")
    print(f"🔑 Username: {username}")


def main():
    """Main migration function"""
    print("🚀 BioGraph User Migration Tool")
    print("=" * 50)
    
    while True:
        print("\nSelect an option:")
        print("1. Migrate users from existing MongoDB")
        print("2. Test phone authentication")
        print("3. Create test phone user")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            migrate_users_from_mongodb()
        elif choice == "2":
            test_phone_authentication()
        elif choice == "3":
            create_test_phone_user()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
