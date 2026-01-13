# Machakos University Clearance System

A comprehensive full-stack web application for automating Machakos University's graduation clearance process. The system digitizes the clearance workflow, enabling seamless communication between students, department staff, and administrators.

**Status**: ✅ Production Ready  
**Tech Stack**: Django 4.2.7 + Angular 21.0.0  
**Last Updated**: January 13, 2026

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Test Credentials](#test-credentials)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Features by Role](#features-by-role)
- [Troubleshooting](#troubleshooting)

---

## Overview

The MksU Clearance System streamlines the graduation clearance process by:

- **Automating workflows**: Digital submission and approval process
- **Enabling real-time tracking**: Students and staff track progress instantly
- **Ensuring accountability**: Complete audit trail of all actions
- **Providing insights**: Analytics for administrators to identify bottlenecks
- **Reducing manual work**: Minimal paperwork, automated notifications

### Problem Solved
Traditional clearance involved:
- ❌ Physical paperwork and manual signatures
- ❌ Long queues and delays
- ❌ No centralized tracking
- ❌ Difficulty accessing approval status
- ❌ No historical records for audits

### Our Solution
This system provides:
- ✅ Digital workflow automation
- ✅ Real-time status updates and notifications
- ✅ Role-based access control (Student, Staff, Admin)
- ✅ Complete audit logging
- ✅ Responsive web interface
- ✅ RESTful API for integration

---

## Key Features

### 👨‍🎓 Student Features
- **Unified Login & Registration**: Single entry point for all users
- **Dashboard**: View clearance status across all departments
- **Status Tracking**: Real-time visualization of approval progress
- **Department Cards**: See status per department (Chairperson, Library, Hostel, Finance, etc.)
- **Responsive Design**: Mobile-friendly interface

### 🏢 Department Staff Features
- **Staff Dashboard**: View pending clearance approvals
- **Approval Management**: Approve or reject clearance requests
- **Feedback System**: Add comments and rejection reasons
- **Filtering**: Filter by status (all, approved, pending, rejected)
- **Quick Actions**: Fast approval/rejection workflow

### 🔐 Administrator Features
- **Admin Dashboard**: System-wide statistics and monitoring
- **User Management**: View and manage all users
- **User Deletion**: Remove users from system
- **System Statistics**: Total users, clearances, and approvals count
- **Responsive Controls**: Delete users with confirmation dialogs

### 🔧 Core Features
- **Unified Authentication**: Single login for all three roles
- **Role-Based Routing**: Automatic routing to correct dashboard based on role
- **JWT Token Management**: Secure token-based authentication
- **CORS Enabled**: Frontend and backend communication
- **Token Storage**: Secure localStorage for session management

---

## System Architecture

```
MksU-Clearance-System/
├── BACKEND/
│   ├── apps/
│   │   ├── users/              # Authentication & user management
│   │   ├── students/           # Student profiles & data
│   │   ├── departments/        # Department management
│   │   ├── clearances/         # Clearance requests
│   │   ├── approvals/          # Department approvals
│   │   ├── finance/            # Payment & finance tracking
│   │   ├── notifications/      # Email & in-app notifications
│   │   ├── audit_logs/         # Audit trail middleware
│   │   ├── gown_issuance/      # Gown tracking
│   │   ├── analytics/          # Statistics & reports
│   │   └── academics/          # Academic structure
│   ├── config/                 # Django settings & URL routing
│   ├── scripts/                # Utility scripts
│   ├── db.sqlite3              # SQLite database (development)
│   ├── create_test_users.py    # Test user creation script
│   └── requirements.txt        # Python dependencies
│
└── FRONTEND/
    ├── src/app/
    │   ├── services/           # API service & authentication
    │   ├── student-login/      # Unified login component
    │   ├── student-dashboard/  # Student portal
    │   ├── staff-dashboard/    # Staff portal
    │   ├── admin-dashboard/    # Admin portal
    │   ├── app.routes.ts       # Route definitions
    │   ├── app.config.ts       # App configuration
    │   └── app.component.ts    # Root component
    ├── package.json            # Node dependencies
    ├── angular.json            # Angular configuration
    └── tsconfig.json           # TypeScript configuration
```

---

## Tech Stack

### Backend
- **Language**: Python 3.10+
- **Framework**: Django 4.2.7
- **REST API**: Django REST Framework 3.14.0
- **Authentication**: djangorestframework-simplejwt 5.5.1
- **Database**: SQLite (dev), MySQL 8.0+ (production)
- **ORM**: Django ORM
- **CORS**: django-cors-headers
- **Caching**: In-memory (dev), Redis (production)

### Frontend
- **Framework**: Angular 21.1.0
- **Language**: HTML, CSS, TypeScript
- **HTTP Client**: Angular HttpClient
- **Routing**: Angular Router
- **Styling**: CSS (custom)
- **Build Tool**: Angular CLI

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18.x+
- Git

### Backend Quick Start
```bash
# 1. Navigate to backend
cd BACKEND

# 2. Create and activate Python virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create test users
python create_test_users.py

# 6. Start server
python manage.py runserver 8000
```

Backend available at: **http://127.0.0.1:8000**

### Frontend Quick Start
```bash
# 1. Navigate to frontend
cd FRONTEND

# 2. Install dependencies
npm install

# 3. Start development server
npm start
```

Frontend available at: **http://localhost:4200**

---

## Installation

### Detailed Backend Setup

#### 1. Clone Repository
```bash
git clone https://github.com/MukuaStephen/MksU-Clearance-System.git
cd MksU-Clearance-System
```

#### 2. Create Virtual Environment
```bash
cd BACKEND
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Database Setup (SQLite - Development)
```bash
python manage.py migrate
```

#### 5. Create Test Users
```bash
python create_test_users.py
```

This creates:
- Admin: admin@mksu.ac.ke / admin123
- Staff: staff@mksu.ac.ke / staff123
- Student: student@example.com / password123

### Detailed Frontend Setup

#### 1. Navigate to Frontend
```bash
cd ../FRONTEND
```

#### 2. Install Dependencies
```bash
npm install
```

#### 3. Start Development Server
```bash
npm start
```

The app will automatically open at **http://localhost:4200**

---

## Configuration

### Backend Configuration (`BACKEND/config/settings.py`)

**Database (SQLite)**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv('SQLITE_DB_PATH', 'db.sqlite3'),
    }
}
```

**CORS Configuration**
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
    'http://127.0.0.1:4200',
    'http://localhost:5173',
    'https://clearance.mksu.ac.ke',
]
CORS_ALLOW_CREDENTIALS = True
```

**JWT Configuration**
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ALGORITHM': 'HS256',
}
```

### Frontend Configuration (`FRONTEND/src/app/services/api.service.ts`)

```typescript
private baseUrl = 'http://localhost:8000/api';
```

---

## Running the Application

### Method 1: Two Terminal Windows (Recommended)

**Terminal 1 - Backend**
```bash
cd BACKEND
venv\Scripts\activate
python manage.py runserver 8000
```

**Terminal 2 - Frontend**
```bash
cd FRONTEND
npm start
```

### Method 2: Using Scripts (Windows)

Create `run_servers.bat` in project root:
```batch
@echo off
start cmd /k "cd BACKEND && venv\Scripts\activate && python manage.py runserver 8000"
start cmd /k "cd FRONTEND && npm start"
pause
```

Then run: `run_servers.bat`

---

## Test Credentials

### 🔐 Login URL
**http://localhost:4200/login**

All users login through the same unified login page.

### Admin Account
```
Email:    admin@mksu.ac.ke
Password: admin123
Role:     Administrator
Destination: /admin/dashboard
```

### Staff Account
```
Email:    staff@mksu.ac.ke
Password: staff123
Role:     Department Staff
Destination: /staff/dashboard
```

### Student Account
```
Email:    student@example.com
Password: password123
Role:     Student
Destination: /dashboard
```

### Create Additional Users

**Via Python Script:**
```bash
python manage.py shell
```

```python
from apps.users.models import User

# Create new student
user = User.objects.create_user(
    username='newstudent@example.com',
    email='newstudent@example.com',
    password='password123',
    first_name='John',
    last_name='Doe',
    role='student'
)
user.set_password('password123')
user.save()
print('User created successfully')
```

---

## API Documentation

### Base URL
```
http://localhost:8000/api
```

### Authentication
All endpoints (except login/register) require a Bearer token:
```
Authorization: Bearer <your_access_token>
```

### Key Endpoints

#### Authentication
- `POST /auth/login/` - User login
- `POST /auth/register/` - User registration
- `POST /auth/logout/` - User logout
- `POST /auth/token/refresh/` - Refresh JWT token
- `GET /auth/profile/` - Get current user profile

#### Users
- `GET /users/` - List all users (admin only)
- `GET /users/{id}/` - Get user details
- `DELETE /users/{id}/` - Delete user (admin only)

#### Students
- `GET /students/` - List all students
- `GET /students/{id}/` - Get student profile
- `POST /students/` - Create student (admin only)

#### Clearances
- `GET /clearances/` - List clearances
- `POST /clearances/` - Create clearance request
- `GET /clearances/{id}/` - Get clearance details
- `PUT /clearances/{id}/` - Update clearance

#### Approvals (Staff)
- `GET /approvals/` - List pending approvals
- `POST /approvals/{id}/approve/` - Approve clearance
- `POST /approvals/{id}/reject/` - Reject clearance

### Full API Documentation
Available at: **http://localhost:8000/api/docs/** (Swagger UI)

---

## Project Structure

### Backend Components

**Users App** - Authentication & user management
```
apps/users/
├── models.py          # User model with role-based access
├── views.py           # Login, register, logout endpoints
├── serializers.py     # User data serialization
├── urls.py            # Auth routes
└── migrations/
```

**Students App** - Student profiles
```
apps/students/
├── models.py          # Student model
├── views.py           # Student endpoints
├── serializers.py     # Student serialization
└── urls.py
```

**Clearances App** - Clearance request management
```
apps/clearances/
├── models.py          # Clearance request model
├── views.py           # Clearance endpoints
├── serializers.py     # Clearance serialization
└── urls.py
```

**Approvals App** - Department approval workflow
```
apps/approvals/
├── models.py          # Approval model
├── views.py           # Approval endpoints
├── serializers.py     # Approval serialization
└── urls.py
```

### Frontend Components

**Login Component** - Unified authentication
```
student-login/
├── student-login.component.ts      # Login logic, role-based routing
├── student-login.component.html    # Login form
└── student-login.component.css     # Login styling
```

**Student Dashboard** - Student portal
```
student-dashboard/
├── student-dashboard.component.ts  # Dashboard logic
├── student-dashboard.component.html # Dashboard UI
└── student-dashboard.component.css  # Dashboard styling
```

**Staff Dashboard** - Staff portal
```
staff-dashboard/
├── staff-dashboard.component.ts    # Approval management logic
├── staff-dashboard.component.html  # Approval UI
└── staff-dashboard.component.css   # Approval styling
```

**Admin Dashboard** - Admin portal
```
admin-dashboard/
├── admin-dashboard.component.ts    # User management logic
├── admin-dashboard.component.html  # Admin UI
└── admin-dashboard.component.css   # Admin styling
```

**API Service** - Backend communication
```
services/
├── api.service.ts    # All API endpoints
├── auth.service.ts   # Authentication logic
```

---

## Features by Role

### 🎓 Student Portal (`/dashboard`)
| Feature | Status |
|---------|--------|
| View clearance status | ✅ Active |
| See department progress | ✅ Active |
| View approval/pending/denied status | ✅ Active |
| Visual dashboard with cards | ✅ Active |
| Logout functionality | ✅ Active |

### 👔 Staff Portal (`/staff/dashboard`)
| Feature | Status |
|---------|--------|
| View pending clearances | ✅ Active |
| Approve clearances | ✅ Active |
| Reject clearances | ✅ Active |
| Filter by status | ✅ Active |
| Add feedback/comments | ✅ Active |
| Logout functionality | ✅ Active |

### 🔑 Admin Portal (`/admin/dashboard`)
| Feature | Status |
|---------|--------|
| View system statistics | ✅ Active |
| List all users | ✅ Active |
| Delete users | ✅ Active |
| View user details | ✅ Active |
| System monitoring | ✅ Active |
| Logout functionality | ✅ Active |

---

## Troubleshooting

### Backend Issues

#### 1. "Cannot connect to server" error
**Symptom**: Login button shows error message  
**Solution**:
1. Verify backend is running: `python manage.py runserver 8000`
2. Check CORS settings allow `http://localhost:4200`
3. Ensure both servers are running

#### 2. "Unable to log in with provided credentials"
**Symptom**: Correct credentials are rejected  
**Solution**:
```bash
# Recreate test users
python create_test_users.py

# Or verify user exists:
python manage.py shell
from apps.users.models import User
User.objects.filter(email='admin@mksu.ac.ke').exists()
```

#### 3. Database migration errors
**Symptom**: `django.db.utils.OperationalError`  
**Solution**:
```bash
python manage.py migrate --run-syncdb
```

#### 4. Redis/Cache errors
**Symptom**: `ConnectionRefusedError` when throttling  
**Solution**: Backend uses in-memory cache for development. No action needed.

### Frontend Issues

#### 1. "Cannot find module" errors
**Symptom**: Compilation errors in console  
**Solution**:
```bash
cd FRONTEND
rm -r node_modules package-lock.json
npm install
npm start
```

#### 2. Blank page after login
**Symptom**: Page doesn't load after successful authentication  
**Solution**:
1. Check DevTools Console (F12) for errors
2. Verify token in localStorage: DevTools → Application → Local Storage
3. Hard refresh: Ctrl+Shift+R (or Cmd+Shift+R on Mac)

#### 3. Routes not working
**Symptom**: "Cannot GET /dashboard"  
**Solution**: Ensure you're accessing the app at `http://localhost:4200`, not through direct URL navigation

#### 4. CORS errors
**Symptom**: `No 'Access-Control-Allow-Origin' header`  
**Solution**:
1. Check `BACKEND/config/settings.py` CORS settings
2. Ensure `http://localhost:4200` is in `CORS_ALLOWED_ORIGINS`
3. Restart backend after changes

### Database Issues

#### Reset Database
```bash
# Delete database
rm BACKEND/db.sqlite3

# Recreate
python BACKEND/manage.py migrate

# Create test users
python BACKEND/create_test_users.py
```

---

## Development Workflow

### Adding a New Feature

1. **Backend** - Create endpoint in app views
2. **Backend** - Add serializers for data validation
3. **Backend** - Register routes in urls.py
4. **Frontend** - Add API method in api.service.ts
5. **Frontend** - Create component for UI
6. **Frontend** - Add route in app.routes.ts
7. **Test** - Verify in browser and Postman

### Code Standards
- **Python**: PEP 8 (4-space indentation)
- **TypeScript**: Angular style guide
- **Git**: Meaningful commit messages

---

## Deployment (Production)

### Backend Deployment

1. **Update Settings**:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

2. **Use Production Database** (MySQL):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mksu_clearance_prod',
        'USER': 'mksu_app',
        'PASSWORD': 'strong_password',
        'HOST': 'prod-db-server',
        'PORT': '3306',
    }
}
```

3. **Collect Static Files**:
```bash
python manage.py collectstatic
```

4. **Run with Production Server** (Gunicorn):
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Frontend Deployment

1. **Build for Production**:
```bash
npm run build
```

2. **Deploy to Web Server** (Nginx example):
```nginx
server {
    listen 80;
    server_name clearance.mksu.ac.ke;
    
    location / {
        root /var/www/html/mksu-clearance;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
}
```

---

## Support

For issues, questions, or contributions:
1. Check Troubleshooting section
2. Review existing GitHub issues
3. Contact development team

---

## Project Metadata

| Property | Value |
|----------|-------|
| **Repository** | [MksU-Clearance-System](https://github.com/MukuaStephen/MksU-Clearance-System) |
| **Status** | ✅ Production Ready |
| **Backend Port** | 8000 |
| **Frontend Port** | 4200 |
| **Database** | SQLite (dev), MySQL (production) |
| **Python** | 3.10+ |
| **Node** | 18.x+ |
| **Last Updated** | January 13, 2026 |

---

**Happy Clearing! 🎓**
