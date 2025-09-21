#!/usr/bin/env python3
"""
Script to explore cloned MongoDB Atlas database
This script works with your CLONE database - not production!
"""

import pymongo
import json
import os
from datetime import datetime

def connect_to_clone():
    """Connect to cloned MongoDB Atlas database"""
    
    print("🔒 CLONE Database Explorer")
    print("=" * 50)
    print("⚠️  This script works with your CLONE database - not production!")
    print()
    
    # Get connection details from environment variables
    username = os.getenv('MONGO_CLONE_USERNAME')
    password = os.getenv('MONGO_CLONE_PASSWORD')
    cluster = os.getenv('MONGO_CLONE_CLUSTER')
    database = os.getenv('MONGO_CLONE_DATABASE', 'BioGraphDemo')
    
    if not all([username, password, cluster]):
        print("❌ Missing environment variables!")
        print("Please set the following environment variables for your CLONE:")
        print("  export MONGO_CLONE_USERNAME='your_clone_username'")
        print("  export MONGO_CLONE_PASSWORD='your_clone_password'")
        print("  export MONGO_CLONE_CLUSTER='clone-cluster0.abc123'")
        print("  export MONGO_CLONE_DATABASE='BioGraphDemo'  # optional")
        print()
        print("Example:")
        print("  export MONGO_CLONE_USERNAME='biograph_clone_user'")
        print("  export MONGO_CLONE_PASSWORD='your_password'")
        print("  export MONGO_CLONE_CLUSTER='clone-cluster0.abc123'")
        print("  python3 explore_clone_db.py")
        return None, None
    
    # Construct connection string
    connection_string = f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/{database}"
    
    try:
        print(f"🔍 Connecting to CLONE: {cluster}.mongodb.net")
        print("📖 This is your CLONE database - safe to explore!")
        
        client = pymongo.MongoClient(connection_string)
        # Test connection
        client.admin.command('ping')
        print(f"✅ Connected successfully to CLONE database!")
        
        return client, database
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        print("\nPlease check:")
        print("1. Clone database credentials are correct")
        print("2. Clone cluster name is correct")
        print("3. Your IP is whitelisted in the clone cluster")
        print("4. Clone database name is correct")
        return None, None

def explore_clone_database(client, database_name):
    """Explore the clone database structure"""
    
    if not client:
        return
    
    print(f"\n📊 Exploring CLONE database: {database_name}")
    
    # Connect to the database
    db = client[database_name]
    
    # List collections
    collections = db.list_collection_names()
    print(f"\nCollections found: {collections}")
    
    # Explore each collection
    for collection_name in collections:
        collection = db[collection_name]
        count = collection.count_documents({})
        print(f"\n📁 {collection_name}: {count} documents")
        
        # Show sample document structure
        if count > 0:
            print(f"Sample document structure:")
            samples = collection.find({}).limit(3)
            for i, sample in enumerate(samples, 1):
                print(f"\n  Document {i}:")
                for key, value in sample.items():
                    if isinstance(value, dict):
                        print(f"    {key}: {type(value).__name__} with {len(value)} fields")
                    elif isinstance(value, list):
                        print(f"    {key}: list with {len(value)} items")
                    else:
                        # Show more details since this is a clone
                        value_str = str(value)
                        if len(value_str) > 200:
                            value_str = value_str[:200] + "..."
                        print(f"    {key}: {value_str}")

def analyze_clone_users(client, database_name):
    """Analyze user data in clone"""
    
    if not client:
        return
    
    print("\n👥 Analyzing user data in CLONE...")
    
    db = client[database_name]
    
    # Look for user collections
    user_collections = [name for name in db.list_collection_names() if 'user' in name.lower()]
    
    if not user_collections:
        print("❌ No user collections found")
        return
    
    for collection_name in user_collections:
        collection = db[collection_name]
        count = collection.count_documents({})
        print(f"\n👤 {collection_name}: {count} users")
        
        if count > 0:
            # Get sample users
            users = collection.find({}).limit(10)
            print(f"Sample users:")
            for i, user in enumerate(users, 1):
                print(f"\n  User {i}:")
                print(f"    Username: {user.get('username', 'N/A')}")
                print(f"    Phone: {user.get('phone_number', 'N/A')}")
                print(f"    Name: {user.get('name', 'N/A')}")
                print(f"    Email: {user.get('email', 'N/A')}")
                print(f"    Created: {user.get('created_time', 'N/A')}")
                print(f"    ID: {user.get('_id', 'N/A')}")

def analyze_clone_biographs(client, database_name):
    """Analyze biograph content in clone"""
    
    if not client:
        return
    
    print("\n📚 Analyzing biograph content in CLONE...")
    
    db = client[database_name]
    
    # Check biograph collections
    biograph_collections = [name for name in db.list_collection_names() if 'biograph' in name.lower()]
    
    if not biograph_collections:
        print("❌ No biograph collections found")
        return
    
    for collection_name in biograph_collections:
        collection = db[collection_name]
        count = collection.count_documents({})
        print(f"\n📖 {collection_name}: {count} biographs")
        
        if count > 0:
            # Get sample biographs
            biographs = collection.find({}).limit(5)
            print(f"Sample biographs:")
            for i, biograph in enumerate(biographs, 1):
                print(f"\n  Biograph {i}:")
                print(f"    Title: {biograph.get('title', 'N/A')}")
                print(f"    User ID: {biograph.get('user_id', 'N/A')}")
                print(f"    Type: {biograph.get('biograph_type', 'N/A')}")
                print(f"    Created: {biograph.get('created_date', 'N/A')}")
                print(f"    Published: {biograph.get('is_published', 'N/A')}")
                
                # Check for file URLs
                file_fields = ['photo_url', 'record_url', 'video_url']
                for field in file_fields:
                    if field in biograph and biograph[field]:
                        print(f"    {field}: {biograph[field]}")

def check_clone_file_storage(client, database_name):
    """Check file storage references in clone"""
    
    if not client:
        return
    
    print("\n📁 Checking file storage references in CLONE...")
    
    db = client[database_name]
    
    # Look for file URLs in collections
    collections_with_files = []
    
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        
        # Check for file-related fields
        sample = collection.find_one()
        if sample:
            file_fields = [key for key in sample.keys() if any(word in key.lower() for word in ['url', 'file', 'image', 'audio', 'video'])]
            if file_fields:
                collections_with_files.append((collection_name, file_fields))
    
    print(f"Collections with file references:")
    for collection_name, fields in collections_with_files:
        print(f"  {collection_name}: {fields}")

def save_clone_summary(client, database_name):
    """Save clone exploration summary"""
    
    if not client:
        return
    
    print("\n💾 Saving CLONE exploration summary...")
    
    db = client[database_name]
    collections = db.list_collection_names()
    
    summary = {
        "database_name": database_name,
        "exploration_date": datetime.now().isoformat(),
        "collections": {},
        "total_documents": 0,
        "migration_ready": True
    }
    
    for collection_name in collections:
        collection = db[collection_name]
        count = collection.count_documents({})
        summary["collections"][collection_name] = count
        summary["total_documents"] += count
    
    with open("clone_exploration_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Clone summary saved to clone_exploration_summary.json")
    print(f"📊 Total documents in clone: {summary['total_documents']}")

def main():
    """Main function - Clone database exploration"""
    print("🔒 CLONE Database Explorer")
    print("=" * 50)
    print("⚠️  This script works with your CLONE database - not production!")
    print("✅ Safe to explore, test, and experiment!")
    print()
    
    # Connect to clone
    client, database_name = connect_to_clone()
    
    if client:
        try:
            # Explore clone database structure
            explore_clone_database(client, database_name)
            
            # Analyze users in clone
            analyze_clone_users(client, database_name)
            
            # Analyze biographs in clone
            analyze_clone_biographs(client, database_name)
            
            # Check file storage in clone
            check_clone_file_storage(client, database_name)
            
            # Save clone summary
            save_clone_summary(client, database_name)
            
            print("\n✅ CLONE exploration complete!")
            print("\nNext steps:")
            print("1. Review the clone exploration summary")
            print("2. Create migration scripts for the clone")
            print("3. Test migration on the clone")
            print("4. Once tested, apply to production")
            
        except Exception as e:
            print(f"\n❌ Error during exploration: {e}")
        finally:
            client.close()
    else:
        print("\n❌ Could not connect to clone database")
        print("\nPlease check your clone database credentials and try again")

if __name__ == "__main__":
    main()
