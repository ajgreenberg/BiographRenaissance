#!/usr/bin/env python3
"""
SAFE READ-ONLY script to explore MongoDB Atlas BioGraph data
This script will ONLY READ data - no modifications will be made
"""

import pymongo
import json
from datetime import datetime
import os

def connect_to_atlas_safely():
    """Connect to MongoDB Atlas in read-only mode"""
    
    print("🔒 SAFE READ-ONLY MongoDB Atlas Explorer")
    print("=" * 50)
    print("⚠️  This script will ONLY READ data - no modifications will be made")
    print()
    
    # Get connection details from user
    username = input("MongoDB Atlas Username: ").strip()
    password = input("MongoDB Atlas Password: ").strip()
    cluster = input("Cluster name (e.g., cluster0.abc123): ").strip()
    database = input("Database name (default: BioGraphDemo): ").strip() or "BioGraphDemo"
    
    # Construct connection string with read preference
    connection_string = f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/{database}?readPreference=secondaryPreferred"
    
    try:
        print(f"\n🔍 Connecting to: {cluster}.mongodb.net")
        print("📖 Using READ-ONLY mode...")
        
        client = pymongo.MongoClient(connection_string)
        # Test connection
        client.admin.command('ping')
        print(f"✅ Connected successfully to MongoDB Atlas!")
        
        # Set read preference to ensure we're in read-only mode
        client.read_preference = pymongo.ReadPreference.SECONDARY_PREFERRED
        
        return client, database
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        print("\nPlease check:")
        print("1. Username and password are correct")
        print("2. Cluster name is correct")
        print("3. Your IP is whitelisted in MongoDB Atlas")
        print("4. Database name is correct")
        return None, None

def safe_explore_database(client, database_name):
    """Safely explore the database structure (READ-ONLY)"""
    
    if not client:
        return
    
    print(f"\n📊 SAFELY exploring database: {database_name}")
    print("🔒 READ-ONLY mode - no data will be modified")
    
    # Connect to the database
    db = client[database_name]
    
    # List collections
    collections = db.list_collection_names()
    print(f"\nCollections found: {collections}")
    
    # Explore each collection safely
    for collection_name in collections:
        collection = db[collection_name]
        count = collection.count_documents({})
        print(f"\n📁 {collection_name}: {count} documents")
        
        # Show sample document structure (first 3 documents only)
        if count > 0:
            print(f"Sample document structure (first 3 documents):")
            samples = collection.find({}).limit(3)
            for i, sample in enumerate(samples, 1):
                print(f"\n  Document {i}:")
                for key, value in sample.items():
                    if isinstance(value, dict):
                        print(f"    {key}: {type(value).__name__} with {len(value)} fields")
                    elif isinstance(value, list):
                        print(f"    {key}: list with {len(value)} items")
                    else:
                        # Truncate long values for safety
                        value_str = str(value)
                        if len(value_str) > 100:
                            value_str = value_str[:100] + "..."
                        print(f"    {key}: {value_str}")

def safe_analyze_users(client, database_name):
    """Safely analyze user data (READ-ONLY)"""
    
    if not client:
        return
    
    print("\n👥 SAFELY analyzing user data...")
    
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
            # Get sample users (first 5 only)
            users = collection.find({}).limit(5)
            print(f"Sample users:")
            for i, user in enumerate(users, 1):
                print(f"\n  User {i}:")
                print(f"    Username: {user.get('username', 'N/A')}")
                print(f"    Phone: {user.get('phone_number', 'N/A')}")
                print(f"    Name: {user.get('name', 'N/A')}")
                print(f"    Email: {user.get('email', 'N/A')}")
                print(f"    Created: {user.get('created_time', 'N/A')}")
                print(f"    ID: {user.get('_id', 'N/A')}")

def safe_analyze_biographs(client, database_name):
    """Safely analyze biograph content (READ-ONLY)"""
    
    if not client:
        return
    
    print("\n📚 SAFELY analyzing biograph content...")
    
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
            # Get sample biographs (first 3 only)
            biographs = collection.find({}).limit(3)
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
                        print(f"    {field}: {biograph[field][:50]}...")

def safe_check_file_storage(client, database_name):
    """Safely check file storage references (READ-ONLY)"""
    
    if not client:
        return
    
    print("\n📁 SAFELY checking file storage references...")
    
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

def save_exploration_summary(client, database_name):
    """Save exploration summary for migration planning"""
    
    if not client:
        return
    
    print("\n💾 Saving exploration summary...")
    
    db = client[database_name]
    collections = db.list_collection_names()
    
    summary = {
        "database_name": database_name,
        "exploration_date": datetime.now().isoformat(),
        "collections": {},
        "total_documents": 0
    }
    
    for collection_name in collections:
        collection = db[collection_name]
        count = collection.count_documents({})
        summary["collections"][collection_name] = count
        summary["total_documents"] += count
    
    with open("atlas_exploration_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Exploration summary saved to atlas_exploration_summary.json")
    print(f"📊 Total documents across all collections: {summary['total_documents']}")

def main():
    """Main function - SAFE READ-ONLY exploration"""
    print("🔒 SAFE READ-ONLY BioGraph Atlas Explorer")
    print("=" * 50)
    print("⚠️  This script will ONLY READ data - no modifications will be made")
    print("⚠️  No data will be changed, deleted, or modified")
    print()
    
    # Connect to Atlas safely
    client, database_name = connect_to_atlas_safely()
    
    if client:
        try:
            # Explore database structure safely
            safe_explore_database(client, database_name)
            
            # Analyze users safely
            safe_analyze_users(client, database_name)
            
            # Analyze biographs safely
            safe_analyze_biographs(client, database_name)
            
            # Check file storage safely
            safe_check_file_storage(client, database_name)
            
            # Save exploration summary
            save_exploration_summary(client, database_name)
            
            print("\n✅ SAFE exploration complete!")
            print("\nNext steps:")
            print("1. Review the exploration summary")
            print("2. Plan migration strategy based on data structure")
            print("3. Create migration scripts (when ready)")
            print("4. Test migration on a copy of the data first")
            
        except Exception as e:
            print(f"\n❌ Error during exploration: {e}")
        finally:
            client.close()
    else:
        print("\n❌ Could not connect to database")
        print("\nPlease check your MongoDB Atlas credentials and try again")

if __name__ == "__main__":
    main()
