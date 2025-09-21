#!/usr/bin/env python3
"""
Simple connection test script to debug MongoDB Atlas connection issues
"""

import pymongo
import os

def test_connection():
    """Test MongoDB Atlas connection with detailed error reporting"""
    
    print("🔍 MongoDB Atlas Connection Test")
    print("=" * 50)
    
    # Get credentials
    username = os.getenv('MONGO_CLONE_USERNAME', 'Admin')
    password = os.getenv('MONGO_CLONE_PASSWORD', 'KoolKiteKan29')
    cluster = os.getenv('MONGO_CLONE_CLUSTER', 'biographrenaissance.kmwgt23')
    database = os.getenv('MONGO_CLONE_DATABASE', 'biograph-preprod')
    
    print(f"Testing connection with:")
    print(f"  Username: {username}")
    print(f"  Password: {'*' * len(password)}")
    print(f"  Cluster: {cluster}")
    print(f"  Database: {database}")
    print()
    
    # Test different connection strings
    connection_strings = [
        f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/{database}",
        f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/",
        f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/{database}?authSource=admin",
        f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/?authSource=admin"
    ]
    
    for i, conn_str in enumerate(connection_strings, 1):
        print(f"Testing connection string {i}:")
        print(f"  {conn_str}")
        
        try:
            client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            print(f"  ✅ SUCCESS!")
            
            # List databases
            print(f"  📊 Available databases:")
            for db_name in client.list_database_names():
                print(f"    - {db_name}")
            
            client.close()
            return True
            
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            print()
    
    return False

def main():
    """Main function"""
    if test_connection():
        print("\n🎉 Connection successful!")
        print("You can now run: python3 explore_clone_db.py")
    else:
        print("\n❌ All connection attempts failed")
        print("\nPlease check:")
        print("1. Your IP is whitelisted in MongoDB Atlas")
        print("2. Username and password are correct")
        print("3. Cluster name is correct")
        print("4. Database name is correct")

if __name__ == "__main__":
    main()
