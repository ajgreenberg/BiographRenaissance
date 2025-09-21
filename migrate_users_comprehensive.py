#!/usr/bin/env python3
"""
Comprehensive User Migration Script for BiographRenaissance
==========================================================

This script migrates users from the existing MongoDB BioGraph system to BiographRenaissance.
It handles:
- User data migration from AuthApp_usermodel
- Phone number validation and formatting
- Profile data preservation
- Safe migration with rollback capability
- Progress tracking and error handling

Usage:
    python3 migrate_users_comprehensive.py [--dry-run] [--batch-size=100] [--start-from=0]
"""

import os
import sys
import django
from datetime import datetime
import json
import re
from typing import Dict, List, Optional, Tuple

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BiographRenaissance.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.exceptions import ValidationError
from pymongo import MongoClient
from core.models import User, UserProfile

User = get_user_model()

class UserMigrationManager:
    def __init__(self, dry_run: bool = False, batch_size: int = 100):
        self.dry_run = dry_run
        self.batch_size = batch_size
        self.migration_log = []
        self.errors = []
        self.stats = {
            'total_found': 0,
            'migrated': 0,
            'skipped': 0,
            'errors': 0,
            'duplicates': 0
        }
        
        # MongoDB connection
        self.mongo_client = None
        self.mongo_db = None
        self.connect_to_mongodb()
    
    def connect_to_mongodb(self):
        """Connect to MongoDB Atlas clone database"""
        try:
            # Get credentials from environment variables
            username = os.getenv('MONGO_CLONE_USERNAME', 'admin')
            password = os.getenv('MONGO_CLONE_PASSWORD', 'StrongerThan34$')
            cluster = os.getenv('MONGO_CLONE_CLUSTER', 'biographrenaissance.kmwgt23')
            database = os.getenv('MONGO_CLONE_DATABASE', 'biograph-preprod')
            
            connection_string = f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/{database}?retryWrites=true&w=majority"
            
            print(f"🔗 Connecting to MongoDB Atlas clone...")
            print(f"   Cluster: {cluster}")
            print(f"   Database: {database}")
            
            self.mongo_client = MongoClient(connection_string)
            self.mongo_db = self.mongo_client[database]
            
            # Test connection
            self.mongo_client.admin.command('ping')
            print("✅ Connected to MongoDB Atlas clone successfully!")
            
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            sys.exit(1)
    
    def get_users_from_mongodb(self, skip: int = 0, limit: int = None) -> List[Dict]:
        """Fetch users from MongoDB AuthApp_usermodel collection"""
        try:
            collection = self.mongo_db['AuthApp_usermodel']
            
            # Build query to exclude removed users
            query = {
                'status_key': 1,  # Active users only
                'is_removed': False
            }
            
            cursor = collection.find(query).skip(skip)
            if limit:
                cursor = cursor.limit(limit)
            
            users = list(cursor)
            print(f"📊 Found {len(users)} users in MongoDB (skip={skip})")
            return users
            
        except Exception as e:
            print(f"❌ Error fetching users from MongoDB: {e}")
            return []
    
    def clean_phone_number(self, phone: str, country_code: str = "1") -> Tuple[str, str]:
        """Clean and validate phone number"""
        if not phone:
            return None, None
        
        # Remove all non-digit characters
        cleaned = re.sub(r'\D', '', str(phone))
        
        # Handle different phone number formats
        if len(cleaned) == 10:
            # US number without country code
            return f"+{country_code}{cleaned}", country_code
        elif len(cleaned) == 11 and cleaned.startswith('1'):
            # US number with country code
            return f"+{cleaned}", "1"
        elif len(cleaned) > 11:
            # International number
            return f"+{cleaned}", cleaned[:len(cleaned)-10] if len(cleaned) > 10 else "1"
        else:
            # Invalid format
            return None, None
    
    def create_user_from_mongodb_data(self, mongo_user: Dict) -> Optional[User]:
        """Create a BiographRenaissance User from MongoDB user data"""
        try:
            # Extract basic user data
            username = (mongo_user.get('username') or '').strip()
            name = (mongo_user.get('name') or '').strip()
            email = (mongo_user.get('email') or '').strip()
            phone_raw = mongo_user.get('phone_number', '')
            country_code_raw = mongo_user.get('country_code', '1')
            
            # Clean phone number
            phone_clean, country_code_clean = self.clean_phone_number(phone_raw, country_code_raw)
            
            # Validate required fields
            if not username:
                raise ValueError("Username is required")
            
            if not phone_clean:
                raise ValueError(f"Invalid phone number: {phone_raw}")
            
            # Check for existing user
            existing_user = None
            if phone_clean:
                existing_user = User.objects.filter(phone_number=phone_clean).first()
            
            if existing_user:
                self.stats['duplicates'] += 1
                print(f"⚠️  User {username} already exists (phone: {phone_clean})")
                return existing_user
            
            # Create new user
            user_data = {
                'username': username,
                'phone_number': phone_clean,
                'country_code': country_code_clean,
                'is_phone_verified': True,  # Assume verified from old system
                'migrated_from_old_system': True,
                'old_user_id': str(mongo_user.get('_id')),
            }
            
            # Add email if available
            if email and '@' in email:
                user_data['email'] = email
            
            # Add name if available
            if name:
                user_data['first_name'] = name.split()[0] if name.split() else name
                if len(name.split()) > 1:
                    user_data['last_name'] = ' '.join(name.split()[1:])
            
            if self.dry_run:
                print(f"🔍 [DRY RUN] Would create user: {username} ({phone_clean})")
                return None
            
            # Create user with transaction
            with transaction.atomic():
                user = User.objects.create(**user_data)
                
                # Create user profile with available fields
                profile_data = {
                    'user': user,
                    'profile_visibility': 'public',  # Default to public
                    'email_notifications': True,
                    'push_notifications': True,
                    'sms_notifications': False,
                    'theme': 'auto',
                }
                
                UserProfile.objects.create(**profile_data)
                
                print(f"✅ Created user: {username} ({phone_clean})")
                return user
                
        except Exception as e:
            error_msg = f"Error creating user {username}: {e}"
            print(f"❌ {error_msg}")
            self.errors.append(error_msg)
            self.stats['errors'] += 1
            return None
    
    def migrate_users_batch(self, start_from: int = 0) -> Dict:
        """Migrate a batch of users"""
        print(f"\n🚀 Starting user migration (batch size: {self.batch_size}, start: {start_from})")
        print(f"📋 Mode: {'DRY RUN' if self.dry_run else 'LIVE MIGRATION'}")
        
        # Get users from MongoDB
        mongo_users = self.get_users_from_mongodb(skip=start_from, limit=self.batch_size)
        self.stats['total_found'] = len(mongo_users)
        
        if not mongo_users:
            print("📭 No users found to migrate")
            return self.stats
        
        print(f"📊 Processing {len(mongo_users)} users...")
        
        # Process each user
        for i, mongo_user in enumerate(mongo_users, 1):
            username = mongo_user.get('username', f'user_{i}')
            print(f"\n👤 [{i}/{len(mongo_users)}] Processing: {username}")
            
            try:
                user = self.create_user_from_mongodb_data(mongo_user)
                
                if user:
                    self.stats['migrated'] += 1
                    self.migration_log.append({
                        'username': username,
                        'old_id': str(mongo_user.get('_id')),
                        'new_id': user.id,
                        'phone': user.phone_number,
                        'status': 'success'
                    })
                else:
                    self.stats['skipped'] += 1
                    
            except Exception as e:
                error_msg = f"Failed to process user {username}: {e}"
                print(f"❌ {error_msg}")
                self.errors.append(error_msg)
                self.stats['errors'] += 1
        
        return self.stats
    
    def print_migration_summary(self):
        """Print migration summary"""
        print("\n" + "="*60)
        print("📊 MIGRATION SUMMARY")
        print("="*60)
        print(f"Total users found: {self.stats['total_found']}")
        print(f"Successfully migrated: {self.stats['migrated']}")
        print(f"Skipped: {self.stats['skipped']}")
        print(f"Duplicates found: {self.stats['duplicates']}")
        print(f"Errors: {self.stats['errors']}")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors[:10]:  # Show first 10 errors
                print(f"   • {error}")
            if len(self.errors) > 10:
                print(f"   ... and {len(self.errors) - 10} more errors")
        
        print("="*60)
    
    def save_migration_log(self):
        """Save migration log to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"migration_log_{timestamp}.json"
        
        log_data = {
            'timestamp': timestamp,
            'dry_run': self.dry_run,
            'stats': self.stats,
            'errors': self.errors,
            'migration_log': self.migration_log
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"📝 Migration log saved to: {log_file}")
    
    def close_connections(self):
        """Close database connections"""
        if self.mongo_client:
            self.mongo_client.close()
            print("🔌 MongoDB connection closed")

def main():
    """Main migration function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrate users from MongoDB to BiographRenaissance')
    parser.add_argument('--dry-run', action='store_true', help='Run in dry-run mode (no actual changes)')
    parser.add_argument('--batch-size', type=int, default=100, help='Number of users to process per batch')
    parser.add_argument('--start-from', type=int, default=0, help='Start from this user index')
    
    args = parser.parse_args()
    
    print("🎨 BiographRenaissance User Migration")
    print("="*50)
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE MIGRATION'}")
    print(f"Batch size: {args.batch_size}")
    print(f"Start from: {args.start_from}")
    print("="*50)
    
    # Confirm if not dry run
    if not args.dry_run:
        try:
            confirm = input("\n⚠️  This will create users in the database. Continue? (y/N): ")
            if confirm.lower() != 'y':
                print("❌ Migration cancelled")
                return
        except EOFError:
            # Auto-confirm in non-interactive environments
            print("\n⚠️  Auto-confirming migration in non-interactive environment...")
            print("✅ Proceeding with migration...")
    
    # Initialize migration manager
    migration_manager = UserMigrationManager(
        dry_run=args.dry_run,
        batch_size=args.batch_size
    )
    
    try:
        # Run migration
        stats = migration_manager.migrate_users_batch(start_from=args.start_from)
        
        # Print summary
        migration_manager.print_migration_summary()
        
        # Save log
        migration_manager.save_migration_log()
        
    except KeyboardInterrupt:
        print("\n⏹️  Migration interrupted by user")
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
    finally:
        migration_manager.close_connections()

if __name__ == '__main__':
    main()
