#!/usr/bin/env python3
"""
Test script for Swasthya AI API
"""

import requests
import json
import time

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get('http://localhost:5000/api/health')
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_analyze_meal():
    """Test the meal analysis endpoint"""
    test_data = {
        "food-items": "2 rotis, dal, rice, chicken curry",
        "meal-type": "lunch",
        "portion-size": "medium",
        "age": 30,
        "gender": "male",
        "height": 170,
        "weight": 70,
        "activity-level": "moderate",
        "conditions": ["diabetes"],
        "sleep": 7,
        "water-intake": "2-3l"
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/analyze-meal',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Meal analysis endpoint working")
            result = response.json()
            print(f"Health Score: {result.get('health_score', 'N/A')}")
            print(f"Key Insights: {result.get('key_insights', 'N/A')}")
            print(f"Recommendations: {len(result.get('recommendations', []))} recommendations")
            return True
        else:
            print(f"❌ Meal analysis failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Meal analysis error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Swasthya AI API")
    print("=" * 40)
    
    # Wait a moment for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    health_ok = test_health_endpoint()
    
    # Test meal analysis endpoint
    print("\n2. Testing meal analysis endpoint...")
    meal_ok = test_analyze_meal()
    
    # Summary
    print("\n" + "=" * 40)
    print("Test Summary:")
    print(f"Health endpoint: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Meal analysis: {'✅ PASS' if meal_ok else '❌ FAIL'}")
    
    if health_ok and meal_ok:
        print("\n🎉 All tests passed! The API is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()

