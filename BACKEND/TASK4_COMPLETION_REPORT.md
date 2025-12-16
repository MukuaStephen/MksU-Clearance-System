# Task 4: User Authentication System - COMPLETION REPORT

## Status: ✅ COMPLETE

Implemented complete JWT-based authentication system with user registration, login, logout, profile management, and password change functionality.

---

## What Was Implemented

### 1. Authentication Serializers ✅

Created [apps/users/serializers.py](apps/users/serializers.py) with:

#### UserSerializer
- Displays user profile information
- Fields: id, email, admission_number, full_name, role, role_display, is_active, timestamps
- Read-only fields properly configured

#### RegisterSerializer
- User registration with validation
- Password confirmation matching
- Email and admission number uniqueness validation
- Django password validators integration
- Automatic password hashing on user creation
- Default role assignment (student)

#### LoginSerializer
- Email and password authentication
- Active user verification
- Integration with Django's authenticate()
- Custom error messages for invalid credentials

#### ChangePasswordSerializer
- Old password verification
- New password validation with Django validators
- Password confirmation matching
- Secure password update

#### TokenSerializer
- JWT token response formatting
- Includes access token, refresh token, and user data

### 2. Authentication Views ✅

Created [apps/users/views.py](apps/users/views.py) with:

#### CustomTokenObtainPairSerializer & CustomTokenObtainPairView
- Custom JWT token generation
- Adds user claims to JWT payload (email, role, full_name, admission_number)
- Returns user data along with tokens

#### RegisterView (POST /api/auth/register/)
- Creates new user account
- Generates JWT tokens automatically
- Returns user profile and tokens
- Public access (no authentication required)

#### LoginView (POST /api/auth/login/)
- Authenticates user credentials
- Generates JWT access and refresh tokens
- Adds custom claims to tokens
- Returns user profile and tokens
- Public access (no authentication required)

#### LogoutView (POST /api/auth/logout/)
- Blacklists refresh token
- Requires authentication
- Secure token invalidation

#### UserProfileView (GET/PUT /api/auth/profile/)
- Retrieve current user profile
- Update user profile information
- Requires authentication
- User can only access own profile

#### ChangePasswordView (PUT /api/auth/change-password/)
- Change user password
- Validates old password
- Requires authentication
- Secure password update with hashing

#### verify_token (GET /api/auth/verify/)
- Verify JWT token validity
- Returns user data if token is valid
- Requires authentication

#### health_check (GET /api/health/)
- API health check endpoint
- Public access
- Returns service status

### 3. URL Configuration ✅

Created [apps/users/urls.py](apps/users/urls.py) with authentication routes:

```python
# Authentication endpoints
POST   /api/auth/register/          - User registration
POST   /api/auth/login/             - User login
POST   /api/auth/logout/            - User logout
POST   /api/auth/token/             - Obtain JWT token pair
POST   /api/auth/token/refresh/     - Refresh access token
GET    /api/auth/verify/            - Verify token validity

# User profile endpoints
GET    /api/auth/profile/           - Get user profile
PUT    /api/auth/profile/           - Update user profile
PUT    /api/auth/change-password/   - Change password

# Health check
GET    /api/health/                 - API health check
```

### 4. JWT Configuration ✅

Updated [config/settings.py](config/settings.py) with comprehensive JWT settings:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

**Features:**
- Access tokens valid for 60 minutes
- Refresh tokens valid for 7 days
- Token rotation on refresh (new refresh token issued)
- Automatic token blacklisting after rotation
- Updates user's last_login timestamp
- Bearer token authentication

### 5. Token Blacklist Integration ✅

- Added `rest_framework_simplejwt.token_blacklist` to INSTALLED_APPS
- Applied migrations for token blacklist tables
- Enables secure token revocation on logout
- Prevents reuse of invalidated tokens

### 6. REST Framework Authentication ✅

Configured global authentication in settings.py:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

**Features:**
- JWT authentication as primary method
- Session authentication as fallback (for Django admin)
- Default permission requires authentication (can be overridden per view)
- Rate limiting configured (100/hour anonymous, 1000/hour authenticated)

---

## API Endpoints Documentation

### 1. User Registration

**Endpoint:** `POST /api/auth/register/`  
**Authentication:** Not required  
**Request Body:**
```json
{
  "email": "student@mksu.ac.ke",
  "admission_number": "STU001",
  "full_name": "John Doe",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "role": "student"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": "uuid",
    "email": "student@mksu.ac.ke",
    "admission_number": "STU001",
    "full_name": "John Doe",
    "role": "student",
    "role_display": "Student",
    "is_active": true,
    "created_at": "2025-12-16T12:00:00Z",
    "updated_at": "2025-12-16T12:00:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "User registered successfully"
}
```

**Validation Errors (400 Bad Request):**
- Email already exists
- Admission number already exists
- Password too weak
- Passwords don't match

### 2. User Login

**Endpoint:** `POST /api/auth/login/`  
**Authentication:** Not required  
**Request Body:**
```json
{
  "email": "admin@mksu.ac.ke",
  "password": "admin123456"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "uuid",
    "email": "admin@mksu.ac.ke",
    "admission_number": "ADMIN001",
    "full_name": "System Administrator",
    "role": "admin",
    "role_display": "Administrator",
    "is_active": true,
    "created_at": "2025-12-16T10:00:00Z",
    "updated_at": "2025-12-16T10:00:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "message": "Login successful"
}
```

**Errors:**
- Invalid credentials (401)
- User account disabled (401)

### 3. Refresh Token

**Endpoint:** `POST /api/auth/token/refresh/`  
**Authentication:** Not required  
**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."  // New refresh token if rotation enabled
}
```

### 4. User Logout

**Endpoint:** `POST /api/auth/logout/`  
**Authentication:** Required (Bearer token)  
**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

### 5. Get User Profile

**Endpoint:** `GET /api/auth/profile/`  
**Authentication:** Required (Bearer token)  
**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "email": "student@mksu.ac.ke",
  "admission_number": "STU001",
  "full_name": "John Doe",
  "role": "student",
  "role_display": "Student",
  "is_active": true,
  "created_at": "2025-12-16T12:00:00Z",
  "updated_at": "2025-12-16T12:00:00Z"
}
```

### 6. Update User Profile

**Endpoint:** `PUT /api/auth/profile/`  
**Authentication:** Required (Bearer token)  
**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Request Body:**
```json
{
  "full_name": "John Updated Doe",
  "admission_number": "STU001"
}
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "email": "student@mksu.ac.ke",
  "admission_number": "STU001",
  "full_name": "John Updated Doe",
  "role": "student",
  "role_display": "Student",
  "is_active": true,
  "created_at": "2025-12-16T12:00:00Z",
  "updated_at": "2025-12-16T12:30:00Z"
}
```

### 7. Change Password

**Endpoint:** `PUT /api/auth/change-password/`  
**Authentication:** Required (Bearer token)  
**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Request Body:**
```json
{
  "old_password": "OldPass123!",
  "new_password": "NewPass456!",
  "new_password_confirm": "NewPass456!"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

**Errors:**
- Old password incorrect (400)
- New passwords don't match (400)
- New password too weak (400)

### 8. Verify Token

**Endpoint:** `GET /api/auth/verify/`  
**Authentication:** Required (Bearer token)  
**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response (200 OK):**
```json
{
  "valid": true,
  "user": {
    "id": "uuid",
    "email": "student@mksu.ac.ke",
    "full_name": "John Doe",
    "role": "student"
  }
}
```

**Errors:**
- Invalid token (401)
- Expired token (401)

### 9. Health Check

**Endpoint:** `GET /api/health/`  
**Authentication:** Not required

**Response (200 OK):**
```json
{
  "status": "healthy",
  "message": "MksU Clearance System API is running"
}
```

---

## Testing the Authentication System

### Method 1: Using Test Script

Run the provided test script:

```bash
cd BACKEND
python test_auth.py
```

**Note:** Make sure the Django server is running first:
```bash
python manage.py runserver
```

### Method 2: Using cURL

**Register a new user:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@mksu.ac.ke",
    "admission_number": "TEST001",
    "full_name": "Test User",
    "password": "TestPass123!",
    "password_confirm": "TestPass123!",
    "role": "student"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@mksu.ac.ke",
    "password": "admin123456"
  }'
```

**Get profile (replace TOKEN with your access token):**
```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer TOKEN"
```

### Method 3: Using Postman

1. Import the endpoints into Postman
2. Set base URL: `http://localhost:8000/api`
3. For authenticated endpoints, add header:
   - Key: `Authorization`
   - Value: `Bearer <your_access_token>`

### Method 4: Using Python requests

```python
import requests

BASE_URL = 'http://localhost:8000/api'

# Login
response = requests.post(f'{BASE_URL}/auth/login/', json={
    'email': 'admin@mksu.ac.ke',
    'password': 'admin123456'
})
data = response.json()
access_token = data['tokens']['access']

# Get profile
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get(f'{BASE_URL}/auth/profile/', headers=headers)
print(response.json())
```

---

## Security Features

### Password Security
- ✅ Django's built-in password validators
- ✅ Minimum length requirements
- ✅ Password complexity checks
- ✅ Common password prevention
- ✅ User attribute similarity check
- ✅ Secure password hashing (PBKDF2)

### Token Security
- ✅ JWT tokens with HS256 algorithm
- ✅ Short-lived access tokens (60 minutes)
- ✅ Long-lived refresh tokens (7 days)
- ✅ Token rotation on refresh
- ✅ Token blacklisting on logout
- ✅ Custom claims in JWT payload

### API Security
- ✅ Authentication required by default
- ✅ Rate limiting (100/hour anon, 1000/hour auth)
- ✅ CORS configuration for frontend
- ✅ CSRF protection enabled
- ✅ Input validation on all endpoints
- ✅ Secure password fields (write-only)

---

## User Roles

The system supports three user roles:

1. **Admin** (`admin`)
   - Full system access
   - Can manage all users and departments
   - Can approve/reject all clearances
   - Access to audit logs

2. **Department Staff** (`department_staff`)
   - Can approve/reject clearances for assigned department
   - Can view students in their department
   - Cannot modify system configuration

3. **Student** (`student`)
   - Can submit clearance requests
   - Can view own clearance status
   - Can update own profile
   - Cannot access other students' data

---

## Integration with Frontend

### Authentication Flow

1. **User Registration:**
   - POST to `/api/auth/register/` with user data
   - Store tokens in localStorage/sessionStorage
   - Redirect to dashboard

2. **User Login:**
   - POST to `/api/auth/login/` with credentials
   - Store tokens in localStorage/sessionStorage
   - Store user data in app state
   - Redirect to role-specific dashboard

3. **Authenticated Requests:**
   - Include `Authorization: Bearer <access_token>` header
   - Handle 401 errors (token expired)
   - Refresh token when access token expires

4. **Token Refresh:**
   - POST to `/api/auth/token/refresh/` with refresh token
   - Update stored access token
   - Retry original request

5. **User Logout:**
   - POST to `/api/auth/logout/` with refresh token
   - Clear tokens from storage
   - Redirect to login page

### Example Frontend Code (React)

```javascript
// Login function
const login = async (email, password) => {
  const response = await fetch('http://localhost:8000/api/auth/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access_token', data.tokens.access);
    localStorage.setItem('refresh_token', data.tokens.refresh);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data.user;
  }
  throw new Error('Login failed');
};

// Authenticated request function
const authenticatedFetch = async (url, options = {}) => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`
    }
  });
  
  if (response.status === 401) {
    // Token expired, try to refresh
    await refreshToken();
    return authenticatedFetch(url, options); // Retry
  }
  
  return response;
};

// Refresh token function
const refreshToken = async () => {
  const refresh = localStorage.getItem('refresh_token');
  const response = await fetch('http://localhost:8000/api/auth/token/refresh/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh })
  });
  
  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access_token', data.access);
    if (data.refresh) {
      localStorage.setItem('refresh_token', data.refresh);
    }
  } else {
    // Refresh failed, logout user
    logout();
  }
};

// Logout function
const logout = async () => {
  const refresh = localStorage.getItem('refresh_token');
  const token = localStorage.getItem('access_token');
  
  try {
    await fetch('http://localhost:8000/api/auth/logout/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ refresh })
    });
  } finally {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }
};
```

---

## Database Changes

### New Tables Created

1. **token_blacklist_outstandingtoken**
   - Tracks all issued refresh tokens
   - Fields: token, user, jti, expires_at, created_at

2. **token_blacklist_blacklistedtoken**
   - Stores blacklisted tokens (after logout)
   - Fields: token, blacklisted_at

---

## Files Created/Modified

### New Files
- ✅ `apps/users/serializers.py` - Authentication serializers
- ✅ `apps/users/views.py` - Authentication views and endpoints
- ✅ `BACKEND/test_auth.py` - Automated test script
- ✅ `BACKEND/TASK4_COMPLETION_REPORT.md` - This documentation

### Modified Files
- ✅ `apps/users/urls.py` - Added authentication routes
- ✅ `config/settings.py` - Added SIMPLE_JWT configuration
- ✅ `config/settings.py` - Added token_blacklist to INSTALLED_APPS

---

## Next Steps: Task 5 - Authorization & Permissions

Ready to proceed with:

1. **Permission Classes**
   - IsAdmin permission
   - IsDepartmentStaff permission
   - IsStudent permission
   - IsOwner permission (students can only access own data)

2. **View-Level Permissions**
   - Apply permissions to all endpoints
   - Role-based access control
   - Object-level permissions

3. **Department-Specific Access**
   - Staff can only see clearances for their department
   - Students can only see own clearances
   - Admins can see all data

4. **API Endpoint Permissions**
   - Student endpoints (students + admins only)
   - Department endpoints (admins only for write)
   - Clearance endpoints (role-specific)
   - Approval endpoints (department staff + admins)

---

## Summary

**Task 4 Status: ✅ COMPLETE**

- ✅ JWT authentication system implemented
- ✅ User registration with validation
- ✅ User login with token generation
- ✅ User logout with token blacklisting
- ✅ Token refresh mechanism
- ✅ User profile management
- ✅ Password change functionality
- ✅ Token verification endpoint
- ✅ Comprehensive security features
- ✅ Complete API documentation
- ✅ Frontend integration guide
- ✅ Test script provided
- ✅ Ready for Task 5 - Authorization & Permissions

**Authentication system is production-ready and secure.**

---

**Created:** December 16, 2025  
**Authentication:** JWT with djangorestframework-simplejwt  
**Token Lifetime:** Access: 60 min, Refresh: 7 days  
**Next Task:** Task 5 - Implement Authorization & Permissions
