#!/usr/bin/env python3
"""
Test script for BiographRenaissance authentication endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_register():
    """Test user registration"""
    print("🧪 Testing user registration...")
    
    data = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+1234567890",
        "password": "testpassword123",
        "password_confirm": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=data)
    
    if response.status_code == 201:
        print("✅ Registration successful!")
        result = response.json()
        print(f"User ID: {result['user']['id']}")
        print(f"Email: {result['user']['email']}")
        return result['tokens']['access']
    else:
        print(f"❌ Registration failed: {response.status_code}")
        print(response.text)
        return None

def test_login():
    """Test user login"""
    print("🧪 Testing user login...")
    
    data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=data)
    
    if response.status_code == 200:
        print("✅ Login successful!")
        result = response.json()
        print(f"User ID: {result['user']['id']}")
        return result['tokens']['access']
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        return None

def test_profile(access_token):
    """Test profile endpoint"""
    print("🧪 Testing profile endpoint...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    
    if response.status_code == 200:
        print("✅ Profile retrieval successful!")
        result = response.json()
        print(f"Full name: {result['full_name']}")
        print(f"Email: {result['email']}")
        print(f"Subscription: {result['subscription_status']}")
    else:
        print(f"❌ Profile retrieval failed: {response.status_code}")
        print(response.text)

def test_user_stats(access_token):
    """Test user stats endpoint"""
    print("🧪 Testing user stats endpoint...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/stats/", headers=headers)
    
    if response.status_code == 200:
        print("✅ User stats retrieval successful!")
        result = response.json()
        print(f"Subscription status: {result['subscription_status']}")
        print(f"Is verified: {result['is_verified']}")
    else:
        print(f"❌ User stats retrieval failed: {response.status_code}")
        print(response.text)

def main():
    """Run all tests"""
    print("🚀 Starting BiographRenaissance authentication tests...")
    print("Make sure the Django server is running on http://127.0.0.1:8000")
    print("-" * 50)
    
    # Test registration
    access_token = test_register()
    
    if not access_token:
        # Try login if registration failed (user might already exist)
        access_token = test_login()
    
    if access_token:
        print("-" * 50)
        test_profile(access_token)
        print("-" * 50)
        test_user_stats(access_token)
        print("-" * 50)
        print("🎉 All tests completed!")
    else:
        print("❌ Could not obtain access token. Tests failed.")

if __name__ == "__main__":
    main()
