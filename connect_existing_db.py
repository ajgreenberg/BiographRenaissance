#!/usr/bin/env python3
"""
Script to connect to existing BioGraph MongoDB and explore the data
"""

import pymongo
import json
from datetime import datetime

def connect_to_existing_db():
    """Connect to existing BioGraph MongoDB"""
    
    print("🔍 Connecting to existing BioGraph database...")
    
    # Try different connection methods
    connection_strings = [
        # Local MongoDB
        "mongodb://localhost:27017/",
        # MongoDB Atlas (you'll need to replace with your actual credentials)
        "mongodb+srv://username:password@cluster.mongodb.net/",
        # Alternative local connection
        "mongodb://127.0.0.1:27017/",
    ]
    
    for conn_str in connection_strings:
        try:
            print(f"Trying: {conn_str}")
            client = pymongo.MongoClient(conn_str)
            # Test connection
            client.admin.command('ping')
            print(f"✅ Connected successfully!")
            return client
        except Exception as e:
            print(f"❌ Failed: {e}")
            continue
    
    print("❌ Could not connect to any MongoDB instance")
    return None

def explore_database(client):
    """Explore the existing database structure"""
    
    if not client:
        return
    
    print("\n📊 Exploring existing database...")
    
    # List databases
    databases = client.list_database_names()
    print(f"Available databases: {databases}")
    
    # Connect to BioGraphDemo database
    db = client["BioGraphDemo"]
    
    # List collections
    collections = db.list_collection_names()
    print(f"\nCollections in BioGraphDemo: {collections}")
    
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

def analyze_biograph_content(client):
    """Analyze biograph content structure"""
    
    if not client:
        return
    
    print("\n📚 Analyzing biograph content...")
    
    db = client["BioGraphDemo"]
    
    # Check biograph collections
    biograph_collections = [name for name in db.list_collection_names() if 'biograph' in name.lower()]
    
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

def check_file_storage(client):
    """Check file storage references"""
    
    if not client:
        return
    
    print("\n📁 Checking file storage references...")
    
    db = client["BioGraphDemo"]
    
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

def main():
    """Main function"""
    print("🚀 BioGraph Database Explorer")
    print("=" * 50)
    
    # Connect to database
    client = connect_to_existing_db()
    
    if client:
        # Explore database structure
        explore_database(client)
        
        # Analyze biograph content
        analyze_biograph_content(client)
        
        # Check file storage
        check_file_storage(client)
        
        print("\n✅ Database exploration complete!")
        print("\nNext steps:")
        print("1. Update connection string with your actual MongoDB credentials")
        print("2. Run migration script to transfer users")
        print("3. Create biograph models in BiographRenaissance")
        print("4. Migrate biograph content")
        
        client.close()
    else:
        print("\n❌ Could not connect to database")
        print("\nPlease:")
        print("1. Make sure MongoDB is running locally, OR")
        print("2. Update the connection string with your MongoDB Atlas credentials")

if __name__ == "__main__":
    main()
