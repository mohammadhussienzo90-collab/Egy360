#!/usr/bin/env python3
# FILE: quick_test.py
# ============================================================
"""
Quick API Test Script
Tests all major endpoints to verify API is working

Usage: python quick_test.py
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api/v1"

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_success(message):
    print(f"{GREEN}✅ {message}{RESET}")


def print_error(message):
    print(f"{RED}❌ {message}{RESET}")


def print_info(message):
    print(f"{BLUE}ℹ️  {message}{RESET}")


def print_warning(message):
    print(f"{YELLOW}⚠️  {message}{RESET}")


# Store access token globally
access_token = None


def test_endpoint(method, url, data=None, auth=False, description=""):
    """Test a single endpoint"""
    headers = {"Content-Type": "application/json"}
    if auth and access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)

        if response.status_code in [200, 201]:
            print_success(f"{description}: {response.status_code}")
            return True, response.json()
        else:
            print_error(f"{description}: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False, None
    except Exception as e:
        print_error(f"{description}: {str(e)}")
        return False, None


def main():
    global access_token

    print(f"\n{BLUE}{'=' * 60}")
    print(f"🧪 EGY360 API QUICK TEST")
    print(f"{'=' * 60}{RESET}\n")

    print_info(f"Testing API at: {API_URL}")
    print()

    # Test counters
    total_tests = 0
    passed_tests = 0

    # Test 1: API Documentation
    print(f"\n{YELLOW}📚 Testing API Documentation{RESET}")
    total_tests += 1
    success, _ = test_endpoint(
        "GET",
        f"{BASE_URL}/api/docs/",
        description="Swagger UI"
    )
    if success:
        passed_tests += 1

    # Test 2: Destinations - Cities
    print(f"\n{YELLOW}📍 Testing Destinations API{RESET}")
    total_tests += 1
    success, data = test_endpoint(
        "GET",
        f"{API_URL}/destinations/cities/",
        description="GET /destinations/cities/"
    )
    if success:
        passed_tests += 1
        if data and 'results' in data:
            print_info(f"   Found {len(data['results'])} cities")

    total_tests += 1
    success, _ = test_endpoint(
        "GET",
        f"{API_URL}/destinations/cities/popular/",
        description="GET /destinations/cities/popular/"
    )
    if success:
        passed_tests += 1

    # Test 3: Accommodations
    print(f"\n{YELLOW}🏨 Testing Accommodations API{RESET}")
    total_tests += 1
    success, data = test_endpoint(
        "GET",
        f"{API_URL}/accommodations/accommodations/",
        description="GET /accommodations/accommodations/"
    )
    if success:
        passed_tests += 1
        if data and 'results' in data:
            print_info(f"   Found {len(data['results'])} accommodations")

    total_tests += 1
    success, _ = test_endpoint(
        "GET",
        f"{API_URL}/accommodations/amenities/",
        description="GET /accommodations/amenities/"
    )
    if success:
        passed_tests += 1

    # Test 4: Tours
    print(f"\n{YELLOW}🎫 Testing Tours API{RESET}")
    total_tests += 1
    success, data = test_endpoint(
        "GET",
        f"{API_URL}/tours/tours/",
        description="GET /tours/tours/"
    )
    if success:
        passed_tests += 1
        if data and 'results' in data:
            print_info(f"   Found {len(data['results'])} tours")

    total_tests += 1
    success, _ = test_endpoint(
        "GET",
        f"{API_URL}/tours/categories/",
        description="GET /tours/categories/"
    )
    if success:
        passed_tests += 1

    # Test 5: User Registration
    print(f"\n{YELLOW}👤 Testing User Registration{RESET}")
    username = f"testuser_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    register_data = {
        "username": username,
        "email": f"{username}@test.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "TestPass123!",
        "password2": "TestPass123!",
        "user_type": "tourist"
    }
    total_tests += 1
    success, response = test_endpoint(
        "POST",
        f"{API_URL}/accounts/users/register/",
        data=register_data,
        description="POST /accounts/users/register/"
    )
    if success:
        passed_tests += 1
        if response and 'tokens' in response:
            access_token = response['tokens']['access']
            print_info("   JWT token received")

    # Test 6: User Login
    print(f"\n{YELLOW}🔐 Testing User Login{RESET}")
    login_data = {
        "username": "tourist",
        "password": "tourist123"
    }
    total_tests += 1
    success, response = test_endpoint(
        "POST",
        f"{API_URL}/accounts/users/login/",
        data=login_data,
        description="POST /accounts/users/login/"
    )
    if success:
        passed_tests += 1
        if response and 'tokens' in response:
            access_token = response['tokens']['access']
            print_info("   Logged in as tourist user")

    # Test 7: Get Current User (Authenticated)
    if access_token:
        print(f"\n{YELLOW}👤 Testing Authenticated Endpoints{RESET}")
        total_tests += 1
        success, user_data = test_endpoint(
            "GET",
            f"{API_URL}/accounts/users/me/",
            auth=True,
            description="GET /accounts/users/me/"
        )
        if success:
            passed_tests += 1
            if user_data:
                print_info(f"   User: {user_data.get('username')}")

        # Test 8: Get My Bookings
        total_tests += 1
        success, _ = test_endpoint(
            "GET",
            f"{API_URL}/bookings/bookings/my_bookings/",
            auth=True,
            description="GET /bookings/bookings/my_bookings/"
        )
        if success:
            passed_tests += 1
    else:
        print_warning("Skipping authenticated tests (no token)")

    # Test 9: Reviews
    print(f"\n{YELLOW}⭐ Testing Reviews API{RESET}")
    total_tests += 1
    success, _ = test_endpoint(
        "GET",
        f"{API_URL}/reviews/reviews/",
        description="GET /reviews/reviews/"
    )
    if success:
        passed_tests += 1

    # Test 10: Transportation
    print(f"\n{YELLOW}🚌 Testing Transportation API{RESET}")
    total_tests += 1
    success, _ = test_endpoint(
        "GET",
        f"{API_URL}/transportation/routes/",
        description="GET /transportation/routes/"
    )
    if success:
        passed_tests += 1

    # Test Summary
    print(f"\n{BLUE}{'=' * 60}")
    print(f"📊 TEST SUMMARY")
    print(f"{'=' * 60}{RESET}\n")

    percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    print(f"Total Tests:  {total_tests}")
    print(f"Passed:       {GREEN}{passed_tests}{RESET}")
    print(f"Failed:       {RED}{total_tests - passed_tests}{RESET}")
    print(f"Success Rate: {GREEN if percentage >= 80 else RED}{percentage:.1f}%{RESET}\n")

    if percentage == 100:
        print(f"{GREEN}🎉 ALL TESTS PASSED! Your API is working perfectly!{RESET}")
    elif percentage >= 80:
        print(f"{YELLOW}⚠️  Most tests passed, but some endpoints need attention.{RESET}")
    else:
        print(f"{RED}❌ Many tests failed. Check your setup and try again.{RESET}")

    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Test interrupted by user{RESET}")
    except Exception as e:
        print(f"\n{RED}Error running tests: {str(e)}{RESET}")