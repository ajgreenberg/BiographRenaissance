#!/usr/bin/env python3
"""
Simple script to help set up clone database credentials
"""

import os

def setup_credentials():
    """Help user set up clone database credentials"""
    
    print("🔒 Setting up Clone Database Credentials")
    print("=" * 50)
    print("From your connection string, I can see:")
    print("  Cluster: biographrenaissance.kmwgt23")
    print("  Database: BioGraphDemo (default)")
    print()
    print("Please provide your actual credentials:")
    
    # Get credentials from user
    username = input("Database Username: ").strip()
    password = input("Database Password: ").strip()
    database = input("Database Name (default: BioGraphDemo): ").strip() or "BioGraphDemo"
    
    # Set environment variables
    os.environ['MONGO_CLONE_USERNAME'] = username
    os.environ['MONGO_CLONE_PASSWORD'] = password
    os.environ['MONGO_CLONE_CLUSTER'] = 'biographrenaissance.kmwgt23'
    os.environ['MONGO_CLONE_DATABASE'] = database
    
    print(f"\n✅ Credentials set!")
    print(f"  Username: {username}")
    print(f"  Password: {'*' * len(password)}")
    print(f"  Cluster: biographrenaissance.kmwgt23")
    print(f"  Database: {database}")
    
    # Test connection
    print(f"\n🔍 Testing connection...")
    try:
        import pymongo
        connection_string = f"mongodb+srv://{username}:{password}@biographrenaissance.kmwgt23.mongodb.net/{database}"
        client = pymongo.MongoClient(connection_string)
        client.admin.command('ping')
        print("✅ Connection successful!")
        
        # Show database info
        db = client[database]
        collections = db.list_collection_names()
        print(f"📊 Found {len(collections)} collections: {collections}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Clone Database Setup")
    print("=" * 50)
    
    if setup_credentials():
        print("\n🎉 Setup complete!")
        print("\nNext steps:")
        print("1. Run: python3 explore_clone_db.py")
        print("2. Review your data structure")
        print("3. Plan migration strategy")
    else:
        print("\n❌ Setup failed")
        print("Please check your credentials and try again")

if __name__ == "__main__":
    main()
