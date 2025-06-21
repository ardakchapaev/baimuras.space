from src.utils.logging_config import logger

#!/usr/bin/env python3
"""Test script for form endpoints validation."""

import json
import sys
from urllib.parse import urljoin

import requests

BASE_URL = "http://localhost:5000"


def test_contact_form():
    """Test contact form submission."""
    logger.info("Testing contact form...")

    # Test data
    form_data = {
        "name": "Test User",
        "phone": "+996555123456",
        "email": "test@example.com",
        "service_type": "montessori",
        "message": "Test message for consultation",
    }

    try:
        response = requests.post(
            urljoin(BASE_URL, "/contact"), data=form_data, allow_redirects=False
        )

        if response.status_code in [200, 302]:
            logger.info("✅ Contact form: SUCCESS")
            return True
        else:
            logger.info(f"❌ Contact form: FAILED (Status: {response.status_code})")
            return False

    except requests.exceptions.RequestException as e:
        logger.info(f"❌ Contact form: ERROR - {e}")
        return False


def test_api_consultation():
    """Test API consultation endpoint."""
    logger.info("Testing API consultation endpoint...")

    # Test data
    api_data = {
        "name": "API Test User",
        "contact": "+996555654321",
        "service_type": "kitchens",
        "message": "API test consultation request",
    }

    try:
        response = requests.post(
            urljoin(BASE_URL, "/api/consultation"),
            json=api_data,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                logger.info("✅ API consultation: SUCCESS")
                return True
            else:
                logger.info(f"❌ API consultation: FAILED - {result}")
                return False
        else:
            logger.info(f"❌ API consultation: FAILED (Status: {response.status_code})")
            return False

    except requests.exceptions.RequestException as e:
        logger.info(f"❌ API consultation: ERROR - {e}")
        return False
    except json.JSONDecodeError as e:
        logger.info(f"❌ API consultation: JSON ERROR - {e}")
        return False


def test_registration_form():
    """Test user registration form."""
    logger.info("Testing registration form...")

    # Test data
    reg_data = {
        "username": "testuser123",
        "email": "testuser123@example.com",
        "password": "testpassword123",
    }

    try:
        response = requests.post(
            urljoin(BASE_URL, "/register"), data=reg_data, allow_redirects=False
        )

        if response.status_code in [200, 302]:
            logger.info("✅ Registration form: SUCCESS")
            return True
        else:
            logger.info(
                f"❌ Registration form: FAILED (Status: {response.status_code})"
            )
            return False

    except requests.exceptions.RequestException as e:
        logger.info(f"❌ Registration form: ERROR - {e}")
        return False


def test_server_availability():
    """Test if server is running."""
    logger.info("Checking server availability...")

    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            logger.info("✅ Server is running")
            return True
        else:
            logger.info(f"❌ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.info(f"❌ Server is not available: {e}")
        return False


def main():
    """Run all form tests."""
    logger.info("=== BaiMuras Forms Testing ===\n")

    # Check server availability first
    if not test_server_availability():
        logger.info("\n❌ Cannot proceed with tests - server is not available")
        logger.info("Please start the server with: python -m flask run")
        sys.exit(1)

    logger.info()

    # Run tests
    tests = [test_contact_form, test_api_consultation, test_registration_form]

    results = []
    for test in tests:
        results.append(test())
        logger.info()

    # Summary
    passed = sum(results)
    total = len(results)

    logger.info("=== Test Summary ===")
    logger.info(f"Passed: {passed}/{total}")

    if passed == total:
        logger.info("🎉 All tests passed!")
        sys.exit(0)
    else:
        logger.info("⚠️  Some tests failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
