"""
Comprehensive endpoint test for MksU Clearance System
Tests all API endpoints to verify they are properly connected
"""
import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:8000/api'

def print_test(title, status_code, expected=200):
    """Print test result"""
    symbol = "✓" if status_code == expected else "✗"
    status_text = "PASS" if status_code == expected else "FAIL"
    print(f"{symbol} [{status_text}] {title} - Status: {status_code}")

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("TESTING HEALTH CHECK")
    print("="*60)
    response = requests.get(f'{BASE_URL}/health/')
    print_test("Health Check", response.status_code)
    if response.status_code == 200:
        print(f"  Response: {response.json()}")

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("\n" + "="*60)
    print("TESTING AUTHENTICATION ENDPOINTS")
    print("="*60)
    
    # Test registration
    reg_data = {
        "email": f"test{datetime.now().timestamp()}@mksu.ac.ke",
        "full_name": "Test User",
        "admission_number": "TEST/CS/0001/2024",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
        "role": "student"
    }
    response = requests.post(f'{BASE_URL}/auth/register/', json=reg_data)
    print_test("POST /auth/register/", response.status_code, 201)
    
    if response.status_code == 201:
        data = response.json()
        access_token = data.get('tokens', {}).get('access')
        refresh_token = data.get('tokens', {}).get('refresh')
        
        # Test token verification
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(f'{BASE_URL}/auth/verify/', headers=headers)
        print_test("GET /auth/verify/", response.status_code)
        
        # Test profile
        response = requests.get(f'{BASE_URL}/auth/profile/', headers=headers)
        print_test("GET /auth/profile/", response.status_code)
        
        # Test token refresh
        response = requests.post(f'{BASE_URL}/auth/token/refresh/', json={'refresh': refresh_token})
        print_test("POST /auth/token/refresh/", response.status_code)
        
        return access_token
    
    return None

def test_students_endpoints(token):
    """Test student endpoints"""
    print("\n" + "="*60)
    print("TESTING STUDENT ENDPOINTS")
    print("="*60)
    
    if not token:
        print("  Skipping - no auth token")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # List students
    response = requests.get(f'{BASE_URL}/students/', headers=headers)
    print_test("GET /students/", response.status_code)
    
    # Get own profile
    response = requests.get(f'{BASE_URL}/students/me/', headers=headers)
    print_test("GET /students/me/", response.status_code)

def test_departments_endpoints(token):
    """Test department endpoints"""
    print("\n" + "="*60)
    print("TESTING DEPARTMENT ENDPOINTS")
    print("="*60)
    
    if not token:
        print("  Skipping - no auth token")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # List departments
    response = requests.get(f'{BASE_URL}/departments/', headers=headers)
    print_test("GET /departments/", response.status_code)

def test_clearances_endpoints(token):
    """Test clearance endpoints"""
    print("\n" + "="*60)
    print("TESTING CLEARANCE ENDPOINTS")
    print("="*60)
    
    if not token:
        print("  Skipping - no auth token")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # List clearances
    response = requests.get(f'{BASE_URL}/clearances/', headers=headers)
    print_test("GET /clearances/", response.status_code)

def test_approvals_endpoints(token):
    """Test approval endpoints"""
    print("\n" + "="*60)
    print("TESTING APPROVAL ENDPOINTS")
    print("="*60)
    
    if not token:
        print("  Skipping - no auth token")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # List approvals
    response = requests.get(f'{BASE_URL}/approvals/', headers=headers)
    print_test("GET /approvals/", response.status_code)
    
    # Get pending approvals
    response = requests.get(f'{BASE_URL}/approvals/pending/', headers=headers)
    print_test("GET /approvals/pending/", response.status_code)

def test_finance_endpoints(token):
    """Test finance endpoints"""
    print("\n" + "="*60)
    print("TESTING FINANCE ENDPOINTS")
    print("="*60)
    
    if not token:
        print("  Skipping - no auth token")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # List payments
    response = requests.get(f'{BASE_URL}/finance/payments/', headers=headers)
    print_test("GET /finance/payments/", response.status_code)
    
    # Get own payment
    response = requests.get(f'{BASE_URL}/finance/my_payment/', headers=headers)
    print_test("GET /finance/my_payment/", response.status_code, expected=404)  # Expected 404 if no payment

def test_notifications_endpoints(token):
    """Test notification endpoints"""
    print("\n" + "="*60)
    print("TESTING NOTIFICATION ENDPOINTS")
    print("="*60)
    
    if not token:
        print("  Skipping - no auth token")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # List notifications
    response = requests.get(f'{BASE_URL}/notifications/', headers=headers)
    print_test("GET /notifications/", response.status_code)
    
    # Get unread count
    response = requests.get(f'{BASE_URL}/notifications/unread-count/', headers=headers)
    print_test("GET /notifications/unread-count/", response.status_code)

def test_gown_endpoints(token):
    """Test gown issuance endpoints"""
    print("\n" + "="*60)
    print("TESTING GOWN ISSUANCE ENDPOINTS")
    print("="*60)
    
    if not token:
        print("  Skipping - no auth token")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # List gowns
    response = requests.get(f'{BASE_URL}/gown-issuances/', headers=headers)
    print_test("GET /gown-issuances/", response.status_code)

def test_audit_logs_endpoints(token):
    """Test audit log endpoints"""
    print("\n" + "="*60)
    print("TESTING AUDIT LOG ENDPOINTS")
    print("="*60)
    
    if not token:
        print("  Skipping - no auth token")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # List audit logs
    response = requests.get(f'{BASE_URL}/audit-logs/', headers=headers)
    print_test("GET /audit-logs/", response.status_code)

def test_analytics_endpoints(token):
    """Test analytics endpoints"""
    print("\n" + "="*60)
    print("TESTING ANALYTICS ENDPOINTS")
    print("="*60)
    
    if not token:
        print("  Skipping - no auth token")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Dashboard
    response = requests.get(f'{BASE_URL}/analytics/dashboard/', headers=headers)
    print_test("GET /analytics/dashboard/", response.status_code)
    
    # Completion rate
    response = requests.get(f'{BASE_URL}/analytics/clearance-completion/', headers=headers)
    print_test("GET /analytics/clearance-completion/", response.status_code)
    
    # Bottlenecks
    response = requests.get(f'{BASE_URL}/analytics/department-bottlenecks/', headers=headers)
    print_test("GET /analytics/department-bottlenecks/", response.status_code)
    
    # Financial summary
    response = requests.get(f'{BASE_URL}/analytics/financial-summary/', headers=headers)
    print_test("GET /analytics/financial-summary/", response.status_code)

def test_academics_endpoints(token):
    """Test academics endpoints"""
    print("\n" + "="*60)
    print("TESTING ACADEMICS ENDPOINTS")
    print("="*60)
    
    if not token:
        print("  Skipping - no auth token")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # List schools
    response = requests.get(f'{BASE_URL}/academics/schools/', headers=headers)
    print_test("GET /academics/schools/", response.status_code)
    
    # List departments
    response = requests.get(f'{BASE_URL}/academics/departments/', headers=headers)
    print_test("GET /academics/departments/", response.status_code)
    
    # List courses
    response = requests.get(f'{BASE_URL}/academics/courses/', headers=headers)
    print_test("GET /academics/courses/", response.status_code)

def test_documentation_endpoints():
    """Test API documentation endpoints"""
    print("\n" + "="*60)
    print("TESTING DOCUMENTATION ENDPOINTS")
    print("="*60)
    
    # Swagger UI
    response = requests.get(f'{BASE_URL}/docs/')
    print_test("GET /docs/ (Swagger UI)", response.status_code)
    
    # ReDoc
    response = requests.get(f'{BASE_URL}/redoc/')
    print_test("GET /redoc/", response.status_code)
    
    # OpenAPI Schema
    response = requests.get(f'{BASE_URL}/schema/')
    print_test("GET /schema/ (OpenAPI)", response.status_code)

def main():
    """Run all endpoint tests"""
    print("\n" + "="*60)
    print("MksU CLEARANCE SYSTEM - COMPREHENSIVE ENDPOINT TEST")
    print("="*60)
    print(f"Testing against: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Test health check
        test_health()
        
        # Test documentation
        test_documentation_endpoints()
        
        # Test authentication and get token
        token = test_auth_endpoints()
        
        # Test all other endpoints
        test_students_endpoints(token)
        test_departments_endpoints(token)
        test_clearances_endpoints(token)
        test_approvals_endpoints(token)
        test_finance_endpoints(token)
        test_notifications_endpoints(token)
        test_gown_endpoints(token)
        test_audit_logs_endpoints(token)
        test_analytics_endpoints(token)
        test_academics_endpoints(token)
        
        print("\n" + "="*60)
        print("TESTING COMPLETE")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server")
        print("Make sure Django server is running: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == '__main__':
    main()
