# MksU Clearance System - Frontend Developer Quick Reference

**Purpose:** Quick reference for integrating the frontend with the backend API  
**Target Audience:** Frontend developers (React/Vue/Angular)  
**Date:** January 13, 2026

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [API Base Configuration](#api-base-configuration)
3. [Authentication Flow](#authentication-flow)
4. [Common API Calls](#common-api-calls)
5. [Error Handling](#error-handling)
6. [State Management Examples](#state-management-examples)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Backend Prerequisites

Before starting frontend development, ensure the backend is running:

```bash
cd BACKEND
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend will be available at: **http://localhost:8000**

### API Documentation

Once backend is running, access:

- **Swagger UI (Interactive):** http://localhost:8000/api/docs/
- **ReDoc (HTML):** http://localhost:8000/api/redoc/
- **OpenAPI Schema:** http://localhost:8000/api/schema/

---

## API Base Configuration

### Environment Variables (.env or config)

```javascript
// React example (.env file)
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000  // 30 seconds

// Or in your API service
const API_BASE_URL = process.env.VITE_API_BASE_URL || 'http://localhost:8000'
const API_VERSION = '/api'
```

### API Service Setup (Axios Example)

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: `${process.env.VITE_API_BASE_URL}/api`,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        const refresh = localStorage.getItem('refresh_token')
        const response = await axios.post(
          `${process.env.VITE_API_BASE_URL}/api/auth/token/refresh/`,
          { refresh }
        )
        localStorage.setItem('access_token', response.data.access)
        originalRequest.headers.Authorization = `Bearer ${response.data.access}`
        return api(originalRequest)
      } catch (err) {
        // Refresh failed - logout user
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
      }
    }
    
    return Promise.reject(error)
  }
)

export default api
```

---

## Authentication Flow

### 1. User Registration

```javascript
// POST /api/auth/register/
const register = async (formData) => {
  try {
    const response = await api.post('/auth/register/', {
      email: formData.email,
      full_name: formData.fullName,
      admission_number: formData.registrationNumber,  // Format: SCHOOL/DEPT/NNNN/YYYY
      password: formData.password,
      password_confirm: formData.passwordConfirm,
      role: 'student'  // Default for public registration
    })
    
    // Store tokens
    localStorage.setItem('access_token', response.data.tokens.access)
    localStorage.setItem('refresh_token', response.data.tokens.refresh)
    localStorage.setItem('user', JSON.stringify(response.data.user))
    
    return response.data.user
  } catch (error) {
    throw error.response.data  // Contains validation errors
  }
}
```

### 2. User Login

```javascript
// POST /api/auth/token/ or /api/auth/login/
const login = async (email, password) => {
  try {
    const response = await api.post('/auth/token/', {
      email,
      password
    })
    
    // Store tokens and user data
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)
    localStorage.setItem('user', JSON.stringify(response.data.user))
    
    return response.data.user
  } catch (error) {
    if (error.response?.status === 401) {
      throw new Error('Invalid email or password')
    }
    throw error
  }
}
```

### 3. Get User Profile

```javascript
// GET /api/auth/profile/
const getProfile = async () => {
  try {
    const response = await api.get('/auth/profile/')
    return response.data
  } catch (error) {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/login'
    }
    throw error
  }
}
```

### 4. Logout

```javascript
// POST /api/auth/logout/
const logout = async () => {
  const refresh = localStorage.getItem('refresh_token')
  
  try {
    await api.post('/auth/logout/', { refresh })
  } catch (error) {
    console.error('Logout error:', error)
  } finally {
    // Clear local storage regardless of API response
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    window.location.href = '/login'
  }
}
```

---

## Common API Calls

### Student Endpoints

#### Get Own Profile
```javascript
// GET /api/students/me/
const getMyProfile = async () => {
  const response = await api.get('/students/me/')
  return response.data
}
// Response:
// {
//   id, user, registration_number, admission_year, faculty, program,
//   graduation_year, eligibility_status, school, department, course
// }
```

#### Get Student Clearance Status
```javascript
// GET /api/students/{id}/clearance-status/
const getClearanceStatus = async (studentId) => {
  const response = await api.get(`/students/${studentId}/clearance-status/`)
  return response.data
}
// Response: { clearance_status: "pending|completed|rejected" }
```

### Clearance Endpoints

#### Submit Clearance Request
```javascript
// POST /api/clearances/
const submitClearance = async (studentId) => {
  const response = await api.post('/clearances/', {
    student_id: studentId
  })
  return response.data
}
// Response: ClearanceRequest object with initial status "pending"
```

#### Get Clearance Details
```javascript
// GET /api/clearances/{id}/
const getClearance = async (clearanceId) => {
  const response = await api.get(`/clearances/${clearanceId}/`)
  return response.data
}
// Response includes: status, completion_percentage, approval_summary, payment_status
```

#### Get Clearance Progress
```javascript
// GET /api/clearances/{id}/progress/
const getClearanceProgress = async (clearanceId) => {
  const response = await api.get(`/clearances/${clearanceId}/progress/`)
  return response.data
}
// Response:
// {
//   total_approvals: 8,
//   approved: 5,
//   rejected: 0,
//   pending: 3,
//   completion_percentage: 62.5,
//   approvals: [
//     { department: {name, code}, status, approved_by, approval_date }
//   ]
// }
```

### Approval Endpoints (Staff Only)

#### Get Pending Approvals
```javascript
// GET /api/approvals/pending/
const getPendingApprovals = async () => {
  const response = await api.get('/approvals/pending/')
  return response.data
}
// Response: List of approval objects awaiting action
```

#### Approve Clearance
```javascript
// POST /api/approvals/{id}/approve/
const approveClearance = async (approvalId, notes, evidenceFile) => {
  const formData = new FormData()
  formData.append('notes', notes)
  if (evidenceFile) {
    formData.append('evidence_file', evidenceFile)
  }
  
  const response = await api.post(
    `/approvals/${approvalId}/approve/`,
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  )
  return response.data
}
```

#### Reject Clearance
```javascript
// POST /api/approvals/{id}/reject/
const rejectClearance = async (approvalId, rejectionReason, notes) => {
  const response = await api.post(`/approvals/${approvalId}/reject/`, {
    rejection_reason: rejectionReason,
    notes: notes
  })
  return response.data
}
```

### Finance Endpoints

#### Get Own Payment Status
```javascript
// GET /api/finance/my_payment/
const getMyPayment = async () => {
  try {
    const response = await api.get('/finance/my_payment/')
    return response.data
  } catch (error) {
    if (error.response?.status === 404) {
      return { has_paid: false }  // No payment record yet
    }
    throw error
  }
}
// Response:
// {
//   id, student_id, amount, payment_method, transaction_id,
//   phone_number, payment_date, is_verified, verification_date
// }
```

#### Submit Payment
```javascript
// POST /api/finance/payments/
const submitPayment = async (studentId, amount, paymentData) => {
  const response = await api.post('/finance/payments/', {
    student_id: studentId,
    amount: amount,  // e.g., "5500.00"
    payment_method: paymentData.method,  // "mpesa", "bank", or "cash"
    transaction_id: paymentData.transactionId,
    phone_number: paymentData.phoneNumber  // For M-PESA
  })
  return response.data
}
```

### Notification Endpoints

#### Get Notifications
```javascript
// GET /api/notifications/
const getNotifications = async (page = 1) => {
  const response = await api.get('/notifications/', {
    params: { page }
  })
  return response.data
}
// Response: { count, next, previous, results: [notification, ...] }
```

#### Get Unread Count
```javascript
// GET /api/notifications/unread-count/
const getUnreadCount = async () => {
  const response = await api.get('/notifications/unread-count/')
  return response.data.unread_count
}
```

#### Mark Notification as Read
```javascript
// PUT /api/notifications/{id}/mark-read/
const markNotificationRead = async (notificationId) => {
  const response = await api.put(`/notifications/${notificationId}/mark-read/`)
  return response.data
}
```

#### Mark All Notifications as Read
```javascript
// POST /api/notifications/mark-all-read/
const markAllNotificationsRead = async () => {
  const response = await api.post('/notifications/mark-all-read/')
  return response.data
}
```

### Gown Issuance Endpoints

#### Get Own Gown Info
```javascript
// GET /api/gown-issuances/?student_id={id}
const getMyGown = async (studentId) => {
  const response = await api.get('/gown-issuances/', {
    params: { student_id: studentId }
  })
  return response.data.results[0]  // Get first result
}
// Response:
// {
//   id, student_id, gown_size, gown_code, issue_date, return_date,
//   deposit_amount, deposit_paid, deposit_status, is_returned
// }
```

### Department Endpoints

#### Get All Departments
```javascript
// GET /api/departments/
const getDepartments = async () => {
  const response = await api.get('/departments/')
  return response.data
}
// Response: List of all active departments in clearance order
```

---

## Error Handling

### Error Response Format

```javascript
// The API returns errors in this format:
{
  "detail": "Error message",
  "code": "error_code"
  // OR for validation errors:
  "field_name": ["error message"]
}
```

### Error Handler Utility

```javascript
const handleApiError = (error) => {
  if (error.response) {
    const status = error.response.status
    const data = error.response.data
    
    switch (status) {
      case 400:
        // Validation error
        return {
          type: 'validation',
          errors: data  // Field-level errors
        }
      case 401:
        // Unauthorized - token expired or invalid
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return { type: 'auth', message: 'Please log in again' }
      case 403:
        // Forbidden - no permission
        return { type: 'permission', message: 'You do not have permission' }
      case 404:
        // Not found
        return { type: 'not_found', message: data.detail || 'Resource not found' }
      case 500:
        // Server error
        return { type: 'server', message: 'Server error. Please try again later.' }
      default:
        return { type: 'error', message: data.detail || 'An error occurred' }
    }
  }
  return { type: 'network', message: 'Network error. Check your connection.' }
}
```

### Usage in Components

```javascript
const handleSubmit = async (formData) => {
  try {
    const response = await submitClearance(studentId)
    // Success - show message and redirect
    notification.success('Clearance submitted successfully')
    navigate('/dashboard')
  } catch (error) {
    const errorInfo = handleApiError(error)
    notification.error(errorInfo.message)
    
    if (errorInfo.type === 'validation') {
      setFieldErrors(errorInfo.errors)
    }
  }
}
```

---

## State Management Examples

### React Context API (Recommended for this app)

```javascript
// authContext.js
import React, { createContext, useState, useEffect } from 'react'
import api from './api'

export const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Check if user is logged in
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
    setLoading(false)
  }, [])

  const login = async (email, password) => {
    try {
      setLoading(true)
      const response = await api.post('/auth/token/', { email, password })
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
      localStorage.setItem('user', JSON.stringify(response.data.user))
      setUser(response.data.user)
      return response.data.user
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
      throw err
    } finally {
      setLoading(false)
    }
  }

  const logout = async () => {
    try {
      const refresh = localStorage.getItem('refresh_token')
      await api.post('/auth/logout/', { refresh })
    } finally {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      setUser(null)
    }
  }

  return (
    <AuthContext.Provider value={{ user, loading, error, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
```

### Using Auth in Components

```javascript
import { useContext } from 'react'
import { AuthContext } from './authContext'

function Dashboard() {
  const { user, logout } = useContext(AuthContext)

  if (!user) return <Navigate to="/login" />

  return (
    <div>
      <h1>Welcome, {user.full_name}</h1>
      <p>Role: {user.role_display}</p>
      <button onClick={logout}>Logout</button>
    </div>
  )
}
```

---

## Pagination

Most list endpoints support pagination:

```javascript
// GET /api/clearances/?page=1&page_size=50
const getClearances = async (page = 1, pageSize = 20) => {
  const response = await api.get('/clearances/', {
    params: { page, page_size: pageSize }
  })
  return {
    count: response.data.count,
    next: response.data.next,
    previous: response.data.previous,
    results: response.data.results
  }
}
```

---

## File Upload

For endpoints that accept file uploads (like evidence documents):

```javascript
const uploadEvidence = async (approvalId, file) => {
  const formData = new FormData()
  formData.append('evidence_file', file)
  formData.append('notes', 'Evidence document')

  const response = await api.post(
    `/approvals/${approvalId}/approve/`,
    formData,
    {
      headers: { 'Content-Type': 'multipart/form-data' }
    }
  )
  return response.data
}

// In a form component:
<input 
  type="file" 
  accept=".pdf,.jpg,.jpeg,.png"
  onChange={(e) => uploadEvidence(approvalId, e.target.files[0])}
/>
```

---

## WebSocket for Real-Time Notifications (Optional)

The API also supports WebSocket for real-time notifications (if configured):

```javascript
// Connect to WebSocket
const connectWebSocket = (userId) => {
  const ws = new WebSocket(
    `ws://localhost:8000/ws/notifications/${userId}/`
  )

  ws.onmessage = (event) => {
    const notification = JSON.parse(event.data)
    // Handle notification
    console.log('New notification:', notification)
  }

  ws.onclose = () => {
    console.log('WebSocket closed')
    // Attempt to reconnect
    setTimeout(() => connectWebSocket(userId), 3000)
  }

  return ws
}
```

---

## Troubleshooting

### Issue: CORS Error
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
- Ensure backend is running
- Check that frontend URL is in CORS_ALLOWED_ORIGINS in backend settings
- Update `.env` in BACKEND:
  ```
  CORS_ALLOWED_ORIGINS=http://localhost:5173
  ```

### Issue: 401 Unauthorized
```
"detail": "Unauthorized"
```

**Solution:**
- Check token is being sent in Authorization header
- Verify token hasn't expired
- Token format should be: `Bearer <token>` (note the space)

### Issue: Token Expired
```
"detail": "Token is invalid or expired"
```

**Solution:**
- Implement token refresh mechanism (included in example above)
- Clear localStorage and have user login again

### Issue: 403 Forbidden
```
"detail": "You do not have permission to perform this action"
```

**Solution:**
- Check user role matches required role
- Admin endpoints require `role == 'admin'`
- Staff endpoints require `role == 'department_staff'`
- Student endpoints require `role == 'student'`

### Issue: File Upload Not Working
```
413 Request Entity Too Large
```

**Solution:**
- Max file size is 5MB
- Check file type is allowed (PDF, JPG, PNG)
- Ensure Content-Type header is `multipart/form-data` (not `application/json`)

### Issue: Backend Returns 500 Error
```
"detail": "Server error"
```

**Solution:**
- Check backend console for error details
- Verify database is running
- Check `.env` configuration
- Run: `python manage.py migrate`

---

## Testing Endpoints with Postman

1. **Set Base URL:**
   ```
   {{base_url}} = http://localhost:8000/api
   ```

2. **For authenticated requests:**
   - After login, copy the `access` token
   - In Headers, add: `Authorization: Bearer <token>`

3. **Test workflow:**
   ```
   1. POST /auth/register/ (or /auth/token/ to login)
   2. Copy access token
   3. GET /students/me/
   4. POST /clearances/
   5. GET /approvals/pending/
   6. POST /approvals/{id}/approve/
   ```

---

## Production Deployment Notes

- Change API_BASE_URL to production domain
- Ensure HTTPS is used in production
- Use environment variables for all sensitive data
- Set DEBUG=False in backend settings
- Use a production database (MySQL/PostgreSQL)
- Configure CORS to only allow frontend domain
- Use a reverse proxy (Nginx) in front of Django

---

## Support Resources

- **API Documentation:** http://localhost:8000/api/docs/
- **Backend README:** `BACKEND/README.md`
- **Complete Schema:** `BACKEND/BACKEND_API_SCHEMA.md`
- **Backend Summary:** `BACKEND/COMPLETE_BACKEND_SUMMARY.md`

---

**End of Frontend Quick Reference**
