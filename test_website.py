#!/usr/bin/env python
"""
Automated test script for 360egy.com
Tests all major pages and functionality
"""

import requests
import time
from datetime import datetime

# Website URL
BASE_URL = "https://360egy.com"

# Simple ASCII markers (Windows compatible)
GREEN = ''
RED = ''
YELLOW = ''
RESET = ''

def test_page(url, expected_status=200, page_name="Page"):
    """Test if a page loads correctly"""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        load_time = time.time() - start_time

        if response.status_code == expected_status:
            print(f"[PASS] {page_name}: OK (Status: {response.status_code}, Load time: {load_time:.2f}s)")
            return True
        else:
            print(f"[FAIL] {page_name}: FAILED (Status: {response.status_code})")
            return False
    except requests.exceptions.Timeout:
        print(f"[FAIL] {page_name}: TIMEOUT (>10s)")
        return False
    except Exception as e:
        print(f"[FAIL] {page_name}: ERROR - {str(e)}")
        return False

def test_api_endpoint(url, endpoint_name="API"):
    """Test API endpoint returns JSON"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"[PASS] {endpoint_name}: OK ({len(data)} items)")
            return True
        else:
            print(f"[FAIL] {endpoint_name}: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"[FAIL] {endpoint_name}: ERROR - {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=" * 70)
    print("360EGY.COM - AUTOMATED TEST SUITE")
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()

    results = []

    # Test 1: Homepage
    print("1. TESTING MAIN PAGES")
    print("-" * 70)
    results.append(test_page(f"{BASE_URL}/", page_name="Homepage"))
    results.append(test_page(f"{BASE_URL}/accommodations/", page_name="Accommodations Page"))
    results.append(test_page(f"{BASE_URL}/tours/", page_name="Tours Page"))
    results.append(test_page(f"{BASE_URL}/destinations/", page_name="Destinations Page"))
    results.append(test_page(f"{BASE_URL}/transportation/", page_name="Transportation Page"))
    results.append(test_page(f"{BASE_URL}/blog/", page_name="Blog Page"))
    print()

    # Test 2: Admin Panel
    print("2. TESTING ADMIN PANEL")
    print("-" * 70)
    results.append(test_page(f"{BASE_URL}/admin/", page_name="Admin Login Page"))
    print()

    # Test 3: API Endpoints
    print("3. TESTING API ENDPOINTS")
    print("-" * 70)
    results.append(test_api_endpoint(f"{BASE_URL}/api/accommodations/", endpoint_name="Accommodations API"))
    results.append(test_api_endpoint(f"{BASE_URL}/api/tours/", endpoint_name="Tours API"))
    results.append(test_api_endpoint(f"{BASE_URL}/api/destinations/", endpoint_name="Destinations API"))
    print()

    # Test 4: Static Files
    print("4. TESTING STATIC RESOURCES")
    print("-" * 70)
    results.append(test_page(f"{BASE_URL}/static/", page_name="Static Files", expected_status=404))  # May 404 if no index
    print()

    # Summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    failed = total - passed

    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    if failed > 0:
        print(f"Failed: {failed}")

    percentage = (passed / total) * 100 if total > 0 else 0
    print(f"Success Rate: {percentage:.1f}%")
    print()

    if percentage == 100:
        print("[SUCCESS] ALL TESTS PASSED!")
    elif percentage >= 80:
        print("[WARNING] MOST TESTS PASSED - Some issues need attention")
    else:
        print("[CRITICAL] MULTIPLE FAILURES - Urgent attention needed")

    print("=" * 70)
    print(f"Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

if __name__ == "__main__":
    main()
