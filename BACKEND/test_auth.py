"""
Test script for authentication endpoints
Run with: python test_auth.py
"""
import requests
import json

BASE_URL = 'http://localhost:8000/api'

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f'{BASE_URL}/health/')
    print_response("1. Health Check", response)
    return response.status_code == 200

def test_register():
    """Test user registration"""
    data = {
        "email": "student1@mksu.ac.ke",
        "admission_number": "STU001",
        "full_name": "Test Student One",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
        "role": "student"
    }
    response = requests.post(f'{BASE_URL}/auth/register/', json=data)
    print_response("2. User Registration", response)
    
    if response.status_code == 201:
        return response.json()
    return None

def test_login(email, password):
    """Test user login"""
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(f'{BASE_URL}/auth/login/', json=data)
    print_response("3. User Login", response)
    
    if response.status_code == 200:
        return response.json()
    return None

def test_profile(access_token):
    """Test get user profile"""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(f'{BASE_URL}/auth/profile/', headers=headers)
    print_response("4. Get User Profile", response)
    return response.status_code == 200

def test_verify_token(access_token):
    """Test token verification"""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(f'{BASE_URL}/auth/verify/', headers=headers)
    print_response("5. Verify Token", response)
    return response.status_code == 200

def test_refresh_token(refresh_token):
    """Test token refresh"""
    data = {
        "refresh": refresh_token
    }
    response = requests.post(f'{BASE_URL}/auth/token/refresh/', json=data)
    print_response("6. Refresh Token", response)
    
    if response.status_code == 200:
        return response.json()
    return None

def test_change_password(access_token):
    """Test change password"""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "old_password": "TestPass123!",
        "new_password": "NewPass456!",
        "new_password_confirm": "NewPass456!"
    }
    response = requests.put(f'{BASE_URL}/auth/change-password/', json=data, headers=headers)
    print_response("7. Change Password", response)
    return response.status_code == 200

def test_logout(refresh_token, access_token):
    """Test user logout"""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "refresh": refresh_token
    }
    response = requests.post(f'{BASE_URL}/auth/logout/', json=data, headers=headers)
    print_response("8. User Logout", response)
    return response.status_code == 200

def main():
    """Run all authentication tests"""
    print("\n" + "="*60)
    print("AUTHENTICATION API TESTS")
    print("="*60)
    print("Make sure the Django server is running on localhost:8000")
    print("="*60)
    
    # Test 1: Health Check
    if not test_health_check():
        print("\n❌ Health check failed. Is the server running?")
        return
    
    # Test 2: Register new user
    register_data = test_register()
    if not register_data:
        print("\n❌ Registration failed")
        return
    
    access_token = register_data['tokens']['access']
    refresh_token = register_data['tokens']['refresh']
    email = register_data['user']['email']
    
    # Test 3: Login with existing user
    login_data = test_login('admin@mksu.ac.ke', 'admin123456')
    if login_data:
        admin_access_token = login_data['tokens']['access']
        admin_refresh_token = login_data['tokens']['refresh']
    
    # Test 4: Get user profile
    test_profile(access_token)
    
    # Test 5: Verify token
    test_verify_token(access_token)
    
    # Test 6: Refresh token
    refresh_data = test_refresh_token(refresh_token)
    if refresh_data:
        new_access_token = refresh_data['access']
        print(f"\n✓ New access token generated")
    
    # Test 7: Change password
    test_change_password(access_token)
    
    # Test 8: Logout
    test_logout(refresh_token, access_token)
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60)

if __name__ == '__main__':
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server")
        print("Make sure Django server is running: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
