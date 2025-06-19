#!/usr/bin/env python3
"""Test script for form endpoints validation."""

import requests
import json
import sys
from urllib.parse import urljoin

BASE_URL = "http://localhost:5000"

def test_contact_form():
    """Test contact form submission."""
    print("Testing contact form...")
    
    # Test data
    form_data = {
        'name': 'Test User',
        'phone': '+996555123456',
        'email': 'test@example.com',
        'service_type': 'montessori',
        'message': 'Test message for consultation'
    }
    
    try:
        response = requests.post(
            urljoin(BASE_URL, '/contact'),
            data=form_data,
            allow_redirects=False
        )
        
        if response.status_code in [200, 302]:
            print("✅ Contact form: SUCCESS")
            return True
        else:
            print(f"❌ Contact form: FAILED (Status: {response.status_code})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Contact form: ERROR - {e}")
        return False

def test_api_consultation():
    """Test API consultation endpoint."""
    print("Testing API consultation endpoint...")
    
    # Test data
    api_data = {
        'name': 'API Test User',
        'contact': '+996555654321',
        'service_type': 'kitchens',
        'message': 'API test consultation request'
    }
    
    try:
        response = requests.post(
            urljoin(BASE_URL, '/api/consultation'),
            json=api_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ API consultation: SUCCESS")
                return True
            else:
                print(f"❌ API consultation: FAILED - {result}")
                return False
        else:
            print(f"❌ API consultation: FAILED (Status: {response.status_code})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API consultation: ERROR - {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ API consultation: JSON ERROR - {e}")
        return False

def test_registration_form():
    """Test user registration form."""
    print("Testing registration form...")
    
    # Test data
    reg_data = {
        'username': 'testuser123',
        'email': 'testuser123@example.com',
        'password': 'testpassword123'
    }
    
    try:
        response = requests.post(
            urljoin(BASE_URL, '/register'),
            data=reg_data,
            allow_redirects=False
        )
        
        if response.status_code in [200, 302]:
            print("✅ Registration form: SUCCESS")
            return True
        else:
            print(f"❌ Registration form: FAILED (Status: {response.status_code})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Registration form: ERROR - {e}")
        return False

def test_server_availability():
    """Test if server is running."""
    print("Checking server availability...")
    
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            return True
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Server is not available: {e}")
        return False

def main():
    """Run all form tests."""
    print("=== BaiMuras Forms Testing ===\n")
    
    # Check server availability first
    if not test_server_availability():
        print("\n❌ Cannot proceed with tests - server is not available")
        print("Please start the server with: python -m flask run")
        sys.exit(1)
    
    print()
    
    # Run tests
    tests = [
        test_contact_form,
        test_api_consultation,
        test_registration_form
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=== Test Summary ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
