"""
MongoDB client for BiographRenaissance
Handles direct MongoDB operations for biographs and users
"""

import os
import pymongo
from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

class MongoDBClient:
    """MongoDB client for direct database operations"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self._connected = False
        # Don't connect immediately - use lazy connection
    
    def connect(self):
        """Connect to MongoDB Atlas"""
        if self._connected:
            return
            
        try:
            # Get connection string from environment or use default
            mongodb_uri = os.getenv('MONGODB_URI', 'mongodb+srv://admin:KiteFlyFour78*@biographrenaissance.zkfvhph.mongodb.net/BiographRenaissanceDB?retryWrites=true&w=majority')
            
            self.client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client.get_default_database()
            
            # Test connection with timeout
            self.client.admin.command('ping')
            self._connected = True
            logger.info(f"Connected to MongoDB: {self.db.name}")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            self._connected = False
            # Don't raise exception - allow app to start without MongoDB
    
    def _ensure_connection(self):
        """Ensure MongoDB connection is established"""
        if not self._connected:
            self.connect()
        if not self._connected:
            raise Exception("MongoDB connection failed")
    
    def get_users_collection(self):
        """Get users collection"""
        self._ensure_connection()
        return self.db.AuthApp_usermodel
    
    def get_biographs_collection(self):
        """Get biographs collection"""
        self._ensure_connection()
        return self.db.biographApp_biographmodel
    
    def find_user_by_phone(self, phone_number: str) -> Optional[Dict]:
        """Find user by phone number"""
        try:
            users_collection = self.get_users_collection()
            user = users_collection.find_one({"phone_number": phone_number})
            return user
        except Exception as e:
            logger.error(f"Error finding user by phone: {e}")
            return None
    
    def find_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Find user by MongoDB ObjectId"""
        try:
            users_collection = self.get_users_collection()
            user = users_collection.find_one({"_id": user_id})
            return user
        except Exception as e:
            logger.error(f"Error finding user by ID: {e}")
            return None
    
    def find_user_by_old_id(self, old_user_id: str) -> Optional[Dict]:
        """Find user by old_user_id field (from original database)"""
        try:
            users_collection = self.get_users_collection()
            user = users_collection.find_one({"old_user_id": old_user_id})
            return user
        except Exception as e:
            logger.error(f"Error finding user by old ID: {e}")
            return None
    
    def get_user_biographs(self, user_id: str, limit: int = 20, offset: int = 0) -> List[Dict]:
        """Get biographs for a user using old_user_id approach"""
        try:
            biographs_collection = self.get_biographs_collection()
            
            # First, find the user to get their old_user_id
            user = self.find_user_by_id(user_id)
            if not user or 'old_user_id' not in user:
                logger.error(f"User {user_id} not found or missing old_user_id")
                return []
            
            old_user_id = user['old_user_id']
            
            # Find biographs using the old_user_id (biographs still have original user IDs)
            cursor = biographs_collection.find(
                {"user_id": old_user_id}
            ).sort("created_date", -1).skip(offset).limit(limit)
            
            biographs = list(cursor)
            
            # Convert ObjectId to string for JSON serialization
            for biograph in biographs:
                biograph['_id'] = str(biograph['_id'])
                if 'user_id' in biograph:
                    biograph['user_id'] = str(biograph['user_id'])
            
            return biographs
            
        except Exception as e:
            logger.error(f"Error getting user biographs: {e}")
            return []
    
    def get_user_biographs_by_old_id(self, old_user_id: str, limit: int = 20, offset: int = 0) -> List[Dict]:
        """Get biographs for a user by their old_user_id (direct lookup)"""
        try:
            biographs_collection = self.get_biographs_collection()
            
            # Find biographs using the old_user_id directly
            cursor = biographs_collection.find(
                {"user_id": old_user_id}
            ).sort("created_date", -1).skip(offset).limit(limit)
            
            biographs = list(cursor)
            
            # Convert ObjectId to string for JSON serialization
            for biograph in biographs:
                biograph['_id'] = str(biograph['_id'])
                if 'user_id' in biograph:
                    biograph['user_id'] = str(biograph['user_id'])
            
            return biographs
            
        except Exception as e:
            logger.error(f"Error getting user biographs by old ID: {e}")
            return []
    
    def get_co_authored_biographs(self, old_user_id: str, limit: int = 20, offset: int = 0) -> List[Dict]:
        """Get biographs where user is a co-author"""
        try:
            biographs_collection = self.get_biographs_collection()
            
            # Find biographs where user is in co_authors array
            cursor = biographs_collection.find(
                {"co_authors": old_user_id}
            ).sort("created_date", -1).skip(offset).limit(limit)
            
            biographs = list(cursor)
            
            # Convert ObjectId to string for JSON serialization
            for biograph in biographs:
                biograph['_id'] = str(biograph['_id'])
                if 'user_id' in biograph:
                    biograph['user_id'] = str(biograph['user_id'])
            
            return biographs
            
        except Exception as e:
            logger.error(f"Error getting co-authored biographs: {e}")
            return []
    
    def get_biograph_by_id(self, biograph_id: str) -> Optional[Dict]:
        """Get biograph by ID"""
        try:
            biographs_collection = self.get_biographs_collection()
            biograph = biographs_collection.find_one({"_id": biograph_id})
            
            if biograph:
                # Convert ObjectId to string
                biograph['_id'] = str(biograph['_id'])
                if 'user_id' in biograph:
                    biograph['user_id'] = str(biograph['user_id'])
            
            return biograph
            
        except Exception as e:
            logger.error(f"Error getting biograph by ID: {e}")
            return None
    
    def create_user(self, user_data: Dict) -> Optional[str]:
        """Create a new user"""
        try:
            users_collection = self.get_users_collection()
            
            # Add timestamps
            user_data['created_at'] = datetime.utcnow()
            user_data['updated_at'] = datetime.utcnow()
            
            result = users_collection.insert_one(user_data)
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    def create_biograph(self, biograph_data: Dict) -> Optional[str]:
        """Create a new biograph"""
        try:
            biographs_collection = self.get_biographs_collection()
            
            # Add timestamps
            biograph_data['created_date'] = datetime.utcnow()
            biograph_data['updated_date'] = datetime.utcnow()
            
            result = biographs_collection.insert_one(biograph_data)
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Error creating biograph: {e}")
            return None
    
    def update_biograph(self, biograph_id: str, update_data: Dict) -> bool:
        """Update a biograph"""
        try:
            biographs_collection = self.get_biographs_collection()
            
            # Add update timestamp
            update_data['updated_date'] = datetime.utcnow()
            
            result = biographs_collection.update_one(
                {"_id": biograph_id},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating biograph: {e}")
            return False
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()

# Global instance
mongodb_client = MongoDBClient()
