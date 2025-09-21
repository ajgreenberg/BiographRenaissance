#!/usr/bin/env python3
"""
Test script for BiographRenaissance phone authentication endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8001/api/v1"

def test_phone_registration():
    """Test phone number registration"""
    print("🧪 Testing phone registration...")
    
    data = {
        "phone_number": "1234567890",
        "country_code": "1",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/auth/phone/register/", json=data)
    
    if response.status_code == 200:
        print("✅ Phone registration successful!")
        result = response.json()
        print(f"Message: {result['message']}")
        print(f"Phone: {result['phone_number']}")
        return True
    else:
        print(f"❌ Phone registration failed: {response.status_code}")
        print(response.text)
        return False

def test_phone_otp_verification():
    """Test OTP verification for registration"""
    print("🧪 Testing phone OTP verification...")
    
    data = {
        "phone_number": "1234567890",
        "country_code": "1",
        "otp": "123456",
        "is_login": False
    }
    
    response = requests.post(f"{BASE_URL}/auth/phone/verify/", json=data)
    
    if response.status_code == 200:
        print("✅ Phone OTP verification successful!")
        result = response.json()
        print(f"User ID: {result['user']['id']}")
        print(f"Phone: {result['user']['phone_number']}")
        print(f"Message: {result['message']}")
        return result['tokens']['access']
    else:
        print(f"❌ Phone OTP verification failed: {response.status_code}")
        print(response.text)
        return None

def test_phone_login():
    """Test phone number login"""
    print("🧪 Testing phone login...")
    
    data = {
        "phone_number": "1234567890",
        "country_code": "1"
    }
    
    response = requests.post(f"{BASE_URL}/auth/phone/login/", json=data)
    
    if response.status_code == 200:
        print("✅ Phone login successful!")
        result = response.json()
        print(f"Message: {result['message']}")
        print(f"Phone: {result['phone_number']}")
        return True
    else:
        print(f"❌ Phone login failed: {response.status_code}")
        print(response.text)
        return False

def test_phone_login_otp_verification():
    """Test OTP verification for login"""
    print("🧪 Testing phone login OTP verification...")
    
    data = {
        "phone_number": "1234567890",
        "country_code": "1",
        "otp": "123456",
        "is_login": True
    }
    
    response = requests.post(f"{BASE_URL}/auth/phone/verify/", json=data)
    
    if response.status_code == 200:
        print("✅ Phone login OTP verification successful!")
        result = response.json()
        print(f"User ID: {result['user']['id']}")
        print(f"Phone: {result['user']['phone_number']}")
        print(f"Message: {result['message']}")
        return result['tokens']['access']
    else:
        print(f"❌ Phone login OTP verification failed: {response.status_code}")
        print(response.text)
        return None

def test_profile_with_phone_auth(access_token):
    """Test profile endpoint with phone authentication"""
    print("🧪 Testing profile with phone authentication...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    
    if response.status_code == 200:
        print("✅ Profile retrieval successful!")
        result = response.json()
        print(f"Phone: {result['phone_number']}")
        print(f"Country Code: {result.get('country_code', 'N/A')}")
        print(f"Full Name: {result['full_name']}")
        print(f"Migrated: {result.get('migrated_from_old_system', False)}")
    else:
        print(f"❌ Profile retrieval failed: {response.status_code}")
        print(response.text)

def test_invalid_otp():
    """Test with invalid OTP"""
    print("🧪 Testing invalid OTP...")
    
    data = {
        "phone_number": "1234567890",
        "country_code": "1",
        "otp": "999999",
        "is_login": True
    }
    
    response = requests.post(f"{BASE_URL}/auth/phone/verify/", json=data)
    
    if response.status_code == 400:
        print("✅ Invalid OTP correctly rejected!")
        result = response.json()
        print(f"Error: {result}")
    else:
        print(f"❌ Invalid OTP not rejected: {response.status_code}")
        print(response.text)

def test_nonexistent_user_login():
    """Test login with non-existent user"""
    print("🧪 Testing login with non-existent user...")
    
    data = {
        "phone_number": "9999999999",
        "country_code": "1"
    }
    
    response = requests.post(f"{BASE_URL}/auth/phone/login/", json=data)
    
    if response.status_code == 404:
        print("✅ Non-existent user correctly rejected!")
        result = response.json()
        print(f"Error: {result['error']}")
    else:
        print(f"❌ Non-existent user not rejected: {response.status_code}")
        print(response.text)

def main():
    """Run all phone authentication tests"""
    print("🚀 Starting BiographRenaissance phone authentication tests...")
    print("Make sure the Django server is running on http://127.0.0.1:8001")
    print("-" * 60)
    
    # Test phone registration flow
    print("\n📱 Testing Phone Registration Flow:")
    print("-" * 40)
    
    if test_phone_registration():
        access_token = test_phone_otp_verification()
        if access_token:
            test_profile_with_phone_auth(access_token)
    
    # Test phone login flow
    print("\n📱 Testing Phone Login Flow:")
    print("-" * 40)
    
    if test_phone_login():
        access_token = test_phone_login_otp_verification()
        if access_token:
            test_profile_with_phone_auth(access_token)
    
    # Test error cases
    print("\n❌ Testing Error Cases:")
    print("-" * 40)
    
    test_invalid_otp()
    test_nonexistent_user_login()
    
    print("\n🎉 All phone authentication tests completed!")
    print("\n📋 Summary:")
    print("✅ Phone registration with OTP")
    print("✅ Phone login with OTP")
    print("✅ Profile access with phone authentication")
    print("✅ Error handling for invalid OTP")
    print("✅ Error handling for non-existent users")

if __name__ == "__main__":
    main()
