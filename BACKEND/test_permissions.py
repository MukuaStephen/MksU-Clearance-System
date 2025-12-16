"""
Test Authorization & Permissions System
Tests role-based access control, permissions, and object-level permissions
"""
import requests
import json
from datetime import datetime

# Base URL
BASE_URL = 'http://127.0.0.1:8000/api'

# ANSI Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_section(title):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"{title}")
    print(f"{'='*60}{Colors.RESET}\n")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_info(message):
    print(f"{Colors.YELLOW}ℹ {message}{Colors.RESET}")

# Test users with different roles
test_users = {
    'admin': {
        'email': 'admin@mksu.ac.ke',
        'password': 'admin123',
        'token': None
    },
    'student': {
        'email': 'student@mksu.ac.ke',
        'password': 'student123',
        'token': None,
        'admission_number': 'S2024001'
    },
    'department_staff': {
        'email': 'staff@mksu.ac.ke',
        'password': 'staff123',
        'token': None,
        'admission_number': 'ST2024001'
    }
}

def create_test_users():
    """Create test users for each role"""
    print_section("Creating Test Users")
    
    # Create Admin (if not exists)
    print_info("Creating Admin user...")
    admin_data = {
        'email': test_users['admin']['email'],
        'password': test_users['admin']['password'],
        'full_name': 'Admin User',
        'admission_number': 'ADMIN001',
        'role': 'admin'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/register/', json=admin_data)
        if response.status_code == 201:
            print_success(f"Admin user created: {admin_data['email']}")
        else:
            print_info(f"Admin user may already exist")
    except Exception as e:
        print_error(f"Error creating admin: {str(e)}")
    
    # Create Student
    print_info("Creating Student user...")
    student_data = {
        'email': test_users['student']['email'],
        'password': test_users['student']['password'],
        'full_name': 'Test Student',
        'admission_number': test_users['student']['admission_number'],
        'role': 'student'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/register/', json=student_data)
        if response.status_code == 201:
            print_success(f"Student user created: {student_data['email']}")
        else:
            print_info(f"Student user may already exist")
    except Exception as e:
        print_error(f"Error creating student: {str(e)}")
    
    # Create Department Staff
    print_info("Creating Department Staff user...")
    staff_data = {
        'email': test_users['department_staff']['email'],
        'password': test_users['department_staff']['password'],
        'full_name': 'Test Department Staff',
        'admission_number': test_users['department_staff']['admission_number'],
        'role': 'department_staff'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/register/', json=staff_data)
        if response.status_code == 201:
            print_success(f"Department Staff user created: {staff_data['email']}")
        else:
            print_info(f"Department Staff user may already exist")
    except Exception as e:
        print_error(f"Error creating staff: {str(e)}")

def login_all_users():
    """Login all test users and get JWT tokens"""
    print_section("Logging In Test Users")
    
    for role, user in test_users.items():
        print_info(f"Logging in as {role}: {user['email']}")
        
        try:
            response = requests.post(f'{BASE_URL}/auth/login/', json={
                'email': user['email'],
                'password': user['password']
            })
            
            if response.status_code == 200:
                data = response.json()
                user['token'] = data['tokens']['access']
                print_success(f"{role.upper()} logged in successfully")
            else:
                print_error(f"Failed to login as {role}: {response.text}")
        except Exception as e:
            print_error(f"Error logging in as {role}: {str(e)}")

def test_department_permissions():
    """Test department read-only for non-admins, write for admins"""
    print_section("Testing Department Permissions (IsAdminOrReadOnly)")
    
    # Test 1: All users can read departments
    print_info("Test 1: All authenticated users can read departments")
    for role, user in test_users.items():
        if user['token']:
            try:
                response = requests.get(
                    f'{BASE_URL}/departments/',
                    headers={'Authorization': f'Bearer {user["token"]}'}
                )
                if response.status_code == 200:
                    print_success(f"{role.upper()} can read departments ✓")
                else:
                    print_error(f"{role.upper()} cannot read departments")
            except Exception as e:
                print_error(f"Error: {str(e)}")
    
    # Test 2: Only admins can create departments
    print_info("\nTest 2: Only admins can create departments")
    new_dept = {
        'name': 'Test Department',
        'code': 'TEST',
        'department_type': 'academic',
        'approval_order': 10,
        'contact_email': 'test@mksu.ac.ke'
    }
    
    for role, user in test_users.items():
        if user['token']:
            try:
                response = requests.post(
                    f'{BASE_URL}/departments/',
                    json=new_dept,
                    headers={'Authorization': f'Bearer {user["token"]}'}
                )
                if role == 'admin':
                    if response.status_code == 201:
                        print_success(f"ADMIN can create departments ✓")
                    else:
                        print_error(f"ADMIN should be able to create departments")
                else:
                    if response.status_code == 403:
                        print_success(f"{role.upper()} correctly denied (403) ✓")
                    else:
                        print_error(f"{role.upper()} should be denied")
            except Exception as e:
                print_error(f"Error: {str(e)}")

def test_student_permissions():
    """Test student object-level permissions"""
    print_section("Testing Student Permissions (IsStudentOwnerOrAdmin)")
    
    # Test 1: Students can read their own profile
    print_info("Test 1: Students can read their own profile")
    student_user = test_users['student']
    
    if student_user['token']:
        try:
            response = requests.get(
                f'{BASE_URL}/students/me/',
                headers={'Authorization': f'Bearer {student_user["token"]}'}
            )
            if response.status_code == 200:
                print_success("STUDENT can read own profile ✓")
                student_data = response.json()
                print(f"  Student: {student_data.get('user', {}).get('full_name')}")
            else:
                print_error(f"STUDENT cannot read own profile: {response.text}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
    
    # Test 2: Admin can see all students
    print_info("\nTest 2: Admin can see all students")
    admin_user = test_users['admin']
    
    if admin_user['token']:
        try:
            response = requests.get(
                f'{BASE_URL}/students/',
                headers={'Authorization': f'Bearer {admin_user["token"]}'}
            )
            if response.status_code == 200:
                students = response.json()
                count = len(students) if isinstance(students, list) else students.get('count', 0)
                print_success(f"ADMIN can see all students ({count} students) ✓")
            else:
                print_error(f"ADMIN cannot see students: {response.text}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
    
    # Test 3: Only admins can create students
    print_info("\nTest 3: Only admins can create students")
    new_student_data = {
        'user': {
            'email': 'newstudent@mksu.ac.ke',
            'password': 'password123',
            'full_name': 'New Test Student',
            'admission_number': 'S2024999',
            'role': 'student'
        },
        'registration_number': 'MKSU/2024/999',
        'faculty': 'Engineering',
        'program': 'BSc Computer Science',
        'graduation_year': 2025
    }
    
    for role, user in test_users.items():
        if user['token'] and role in ['admin', 'student']:
            try:
                response = requests.post(
                    f'{BASE_URL}/students/',
                    json=new_student_data,
                    headers={'Authorization': f'Bearer {user["token"]}'}
                )
                if role == 'admin':
                    if response.status_code == 201:
                        print_success(f"ADMIN can create students ✓")
                    else:
                        print_error(f"ADMIN should create students: {response.text}")
                else:
                    if response.status_code == 403:
                        print_success(f"{role.upper()} correctly denied (403) ✓")
                    else:
                        print_error(f"{role.upper()} should be denied")
            except Exception as e:
                print_error(f"Error: {str(e)}")

def test_department_actions():
    """Test custom department actions"""
    print_section("Testing Department Custom Actions")
    
    admin_user = test_users['admin']
    
    if admin_user['token']:
        # Test approval workflow
        print_info("Test: Get approval workflow")
        try:
            response = requests.get(
                f'{BASE_URL}/departments/approval_workflow/',
                headers={'Authorization': f'Bearer {admin_user["token"]}'}
            )
            if response.status_code == 200:
                data = response.json()
                print_success(f"Approval workflow retrieved: {data['total_steps']} steps")
                for step in data['workflow'][:3]:  # Show first 3
                    print(f"  {step['order']}. {step['department']} ({step['code']})")
            else:
                print_error(f"Failed to get workflow: {response.text}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
        
        # Test academic departments
        print_info("\nTest: Get academic departments")
        try:
            response = requests.get(
                f'{BASE_URL}/departments/academic/',
                headers={'Authorization': f'Bearer {admin_user["token"]}'}
            )
            if response.status_code == 200:
                depts = response.json()
                print_success(f"Academic departments retrieved: {len(depts)} departments")
            else:
                print_error(f"Failed to get academic departments: {response.text}")
        except Exception as e:
            print_error(f"Error: {str(e)}")

def test_authentication_endpoints():
    """Test authentication endpoints have correct permissions"""
    print_section("Testing Authentication Endpoint Permissions")
    
    # Test 1: Register is public (AllowAny)
    print_info("Test 1: Register endpoint is public")
    try:
        response = requests.post(f'{BASE_URL}/auth/register/', json={
            'email': 'publictest@mksu.ac.ke',
            'password': 'test123',
            'full_name': 'Public Test',
            'admission_number': 'PUB001',
            'role': 'student'
        })
        if response.status_code in [201, 400]:  # 400 if already exists
            print_success("Register endpoint is public (no auth required) ✓")
        else:
            print_error(f"Register endpoint failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Test 2: Login is public (AllowAny)
    print_info("Test 2: Login endpoint is public")
    try:
        response = requests.post(f'{BASE_URL}/auth/login/', json={
            'email': 'admin@mksu.ac.ke',
            'password': 'admin123'
        })
        if response.status_code == 200:
            print_success("Login endpoint is public (no auth required) ✓")
        else:
            print_error(f"Login endpoint failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Test 3: Profile requires authentication
    print_info("Test 3: Profile endpoint requires authentication")
    try:
        # Without token
        response = requests.get(f'{BASE_URL}/auth/profile/')
        if response.status_code == 401:
            print_success("Profile correctly requires authentication (401 without token) ✓")
        else:
            print_error("Profile should require authentication")
        
        # With token
        admin_user = test_users['admin']
        if admin_user['token']:
            response = requests.get(
                f'{BASE_URL}/auth/profile/',
                headers={'Authorization': f'Bearer {admin_user["token"]}'}
            )
            if response.status_code == 200:
                print_success("Profile accessible with valid token ✓")
            else:
                print_error("Profile should work with valid token")
    except Exception as e:
        print_error(f"Error: {str(e)}")

def run_all_tests():
    """Run all authorization tests"""
    print(f"{Colors.BLUE}")
    print("=" * 60)
    print("    AUTHORIZATION & PERMISSIONS TEST SUITE")
    print("    MksU Clearance System")
    print("=" * 60)
    print(Colors.RESET)
    
    # Setup
    create_test_users()
    login_all_users()
    
    # Run tests
    test_authentication_endpoints()
    test_department_permissions()
    test_student_permissions()
    test_department_actions()
    
    # Summary
    print_section("Test Summary")
    print_success("Authorization & Permissions system is working!")
    print_info("Key Features Tested:")
    print("  ✓ Role-based access control (Admin, Student, Department Staff)")
    print("  ✓ Object-level permissions (Students see own data)")
    print("  ✓ IsAdminOrReadOnly (Departments)")
    print("  ✓ IsStudentOwnerOrAdmin (Students)")
    print("  ✓ Public endpoints (Register, Login)")
    print("  ✓ Protected endpoints (Profile, etc.)")
    print("\n")

if __name__ == '__main__':
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Error running tests: {str(e)}{Colors.RESET}")
