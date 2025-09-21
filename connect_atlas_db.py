#!/usr/bin/env python3
"""
Script to connect to MongoDB Atlas and explore existing BioGraph data
"""

import pymongo
import json
from datetime import datetime

def connect_to_atlas():
    """Connect to MongoDB Atlas"""
    
    print("🔍 Connecting to MongoDB Atlas...")
    print("Please provide your MongoDB Atlas connection details:")
    print("(You can find these in your existing BioGraph app settings)")
    print()
    
    # Get connection details from user
    username = input("MongoDB Username: ").strip()
    password = input("MongoDB Password: ").strip()
    cluster = input("Cluster name (e.g., cluster0.abc123): ").strip()
    database = input("Database name (default: BioGraphDemo): ").strip() or "BioGraphDemo"
    
    # Construct connection string
    connection_string = f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/{database}"
    
    try:
        print(f"\nTrying to connect to: {cluster}.mongodb.net")
        client = pymongo.MongoClient(connection_string)
        # Test connection
        client.admin.command('ping')
        print(f"✅ Connected successfully to MongoDB Atlas!")
        return client, database
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        print("\nPlease check:")
        print("1. Username and password are correct")
        print("2. Cluster name is correct")
        print("3. Your IP is whitelisted in MongoDB Atlas")
        print("4. Database name is correct")
        return None, None

def explore_atlas_database(client, database_name):
    """Explore the Atlas database structure"""
    
    if not client:
        return
    
    print(f"\n📊 Exploring database: {database_name}")
    
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
        
        # Show sample document
        if count > 0:
            sample = collection.find_one()
            print(f"Sample document structure:")
            for key, value in sample.items():
                if isinstance(value, dict):
                    print(f"  {key}: {type(value).__name__} with {len(value)} fields")
                elif isinstance(value, list):
                    print(f"  {key}: list with {len(value)} items")
                else:
                    print(f"  {key}: {type(value).__name__}")
        
        # Show specific fields for user collections
        if 'user' in collection_name.lower():
            print(f"\nUser fields in {collection_name}:")
            users = collection.find({}).limit(3)
            for user in users:
                print(f"  Username: {user.get('username', 'N/A')}")
                print(f"  Phone: {user.get('phone_number', 'N/A')}")
                print(f"  Name: {user.get('name', 'N/A')}")
                print(f"  Created: {user.get('created_time', 'N/A')}")
                print("  ---")

def analyze_biograph_content(client, database_name):
    """Analyze biograph content structure"""
    
    if not client:
        return
    
    print("\n📚 Analyzing biograph content...")
    
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
            sample = collection.find_one()
            print(f"Sample biograph structure:")
            for key, value in sample.items():
                if key in ['title', 'record_text', 'user_id', 'created_date']:
                    print(f"  {key}: {value}")
                elif isinstance(value, dict):
                    print(f"  {key}: {type(value).__name__} with {len(value)} fields")
                elif isinstance(value, list):
                    print(f"  {key}: list with {len(value)} items")

def check_file_storage(client, database_name):
    """Check file storage references"""
    
    if not client:
        return
    
    print("\n📁 Checking file storage references...")
    
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

def save_connection_info(username, password, cluster, database):
    """Save connection info for migration scripts"""
    
    connection_info = {
        "username": username,
        "password": password,
        "cluster": cluster,
        "database": database,
        "connection_string": f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/{database}"
    }
    
    with open("mongodb_connection.json", "w") as f:
        json.dump(connection_info, f, indent=2)
    
    print(f"\n💾 Connection info saved to mongodb_connection.json")
    print("You can use this for migration scripts")

def main():
    """Main function"""
    print("🚀 BioGraph Atlas Database Explorer")
    print("=" * 50)
    
    # Connect to Atlas
    client, database_name = connect_to_atlas()
    
    if client:
        # Explore database structure
        explore_atlas_database(client, database_name)
        
        # Analyze biograph content
        analyze_biograph_content(client, database_name)
        
        # Check file storage
        check_file_storage(client, database_name)
        
        print("\n✅ Database exploration complete!")
        print("\nNext steps:")
        print("1. Run migration script to transfer users")
        print("2. Migrate biograph content")
        print("3. Test phone authentication with migrated users")
        
        client.close()
    else:
        print("\n❌ Could not connect to database")
        print("\nPlease check your MongoDB Atlas credentials and try again")

if __name__ == "__main__":
    main()
