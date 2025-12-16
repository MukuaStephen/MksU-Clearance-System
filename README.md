# Machakos University Clearance System

A comprehensive web-based system for automating Machakos University's graduation clearance process. Built with **React.js** (frontend) and **Django REST Framework** (backend), the system streamlines departmental approvals, integrates finance verification with M-PESA, tracks gown issuance, and provides real-time analytics for administrators and students.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Usage Guide](#usage-guide)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Machakos University Clearance System digitizes and automates the traditionally manual graduation clearance process. Students can submit clearance requests online, track approval progress across multiple departments (Finance, Library, Hostel, Academic, etc.), upload required documents, and receive real-time notifications. Administrators gain powerful analytics and audit trails for compliance and reporting.

### Problem Statement
Traditional clearance processes involve:
- Physical paperwork and manual signatures
- Long queues and delays
- Difficulty tracking approval status
- No centralized record keeping
- Inefficient communication between departments

### Solution
This system provides:
- **Digital workflow** for clearance requests and approvals
- **Real-time tracking** with status updates and notifications
- **Role-based access** for students, department staff, and administrators
- **Financial integration** with M-PESA for graduation fee payments
- **Analytics dashboard** for monitoring bottlenecks and completion rates
- **Audit logging** for compliance and accountability

---

## Key Features

### 👨‍🎓 Student Features
- **User Registration & Authentication** - JWT-based secure login
- **Clearance Request Submission** - Submit requests with supporting documents
- **Real-time Status Tracking** - Monitor approval progress across departments
- **Document Uploads** - Submit evidence files (fee statements, clearance documents)
- **Payment Integration** - M-PESA graduation fee payment (KES 10,000)
- **Gown Issuance Tracking** - Track gown assignment, deposit, and return
- **Email Notifications** - Automated updates on approval status changes

### 🏢 Department Staff Features
- **Approval Workflow** - Approve/reject clearance requests with notes
- **Evidence Review** - Review uploaded documents and evidence files
- **Departmental Dashboard** - View pending approvals and statistics
- **Notes & Rejection Reasons** - Document decisions with detailed feedback

### 🔐 Administrator Features
- **User Management** - Create and manage users (students, staff, admins)
- **Academic Structure** - Manage schools, departments, and courses
- **Department Configuration** - Set approval order and active status
- **Finance Management** - Verify payments and graduation fees
- **Gown Issuance Management** - Track gown assignments, returns, deposits, refunds
- **Analytics & Reporting**:
  - Clearance completion rates by cohort/school
  - Department bottleneck analysis
  - Financial summaries and payment compliance
  - Overall system dashboard with key metrics
- **Audit Logs** - Complete audit trail of all system actions
- **Notification Management** - Send bulk notifications to students

### 🔧 System Features
- **Academic Hierarchy** - Normalized School → AcademicDepartment → Course structure
- **Registration Number Parsing** - Auto-extract admission year from format `SCHOOL/DEPT/NNNN/YYYY`
- **File Upload Validation** - Size limits and format validation (max 5MB for evidence)
- **Graduation Fee Rule** - Enforced KES 10,000 graduation fee at model and API level
- **Multi-tenancy Support** - Filter data by school, department, cohort
- **RESTful API** - Comprehensive API with OpenAPI documentation
- **Responsive Design** - Mobile-friendly interface

---

## System Architecture

### Backend Stack
- **Framework**: Django 4.2.7 + Django REST Framework 3.14
- **Database**: MySQL 8.0+
- **Authentication**: JWT (SimpleJWT)
- **API Documentation**: drf-spectacular (OpenAPI 3.0)
- **Task Queue**: Celery (for background jobs)
- **Cache**: Redis
- **Email**: SMTP (configurable backend)

### Frontend Stack
- **Framework**: React.js 18+
- **Build Tool**: Vite
- **State Management**: React Context/Hooks
- **Routing**: React Router
- **HTTP Client**: Axios
- **Styling**: CSS Modules / Tailwind (if configured)

### Key Components
```
MksU-Clearance-System/
├── BACKEND/
│   ├── apps/
│   │   ├── users/           # Authentication & user management
│   │   ├── students/        # Student profiles
│   │   ├── departments/     # Clearance departments
│   │   ├── academics/       # Schools, departments, courses
│   │   ├── clearances/      # Clearance requests
│   │   ├── approvals/       # Department approvals
│   │   ├── finance/         # Payments & finance records
│   │   ├── gown_issuance/   # Gown tracking
│   │   ├── notifications/   # Email notifications
│   │   ├── audit_logs/      # Audit trail
│   │   └── analytics/       # Dashboards & reports
│   ├── config/              # Django settings & URLs
│   ├── media/               # Uploaded files
│   └── requirements.txt     # Python dependencies
└── FRONTEND/
    ├── src/
    │   ├── components/      # React components
    │   ├── pages/           # Page components
    │   └── App.jsx          # Main app component
    ├── package.json         # Node dependencies
    └── vite.config.js       # Vite configuration
```

---

## Prerequisites

### Required Software
- **Python**: 3.10 or higher
- **Node.js**: 18.x or higher
- **MySQL**: 8.0 or higher
- **Git**: Latest version

### Optional (Recommended)
- **Redis**: 6.x or higher (for caching and Celery)
- **Postman**: For API testing

### System Requirements
- **OS**: Windows 10/11, macOS, or Linux
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space

---

## Installation

### Backend Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/MksU-Clearance-System.git
cd MksU-Clearance-System
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install Python Dependencies
```bash
cd BACKEND
pip install -r requirements.txt
```

#### 4. Configure MySQL Database
```bash
# Login to MySQL as root
mysql -u root -p

# Create database and user
CREATE DATABASE mksu_clearance CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mksu_app'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON mksu_clearance.* TO 'mksu_app'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 5. Configure Environment Variables
Create a `.env` file in the `BACKEND` directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=mksu_clearance
DB_USER=mksu_app
DB_PASSWORD=your_secure_password
DB_HOST=127.0.0.1
DB_PORT=3306

# JWT
JWT_SECRET=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=604800

# Email (for notifications)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# Redis (optional - for production)
REDIS_URL=redis://localhost:6379/0

# M-PESA (for production)
MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_passkey
MPESA_CALLBACK_URL=https://yourdomain.com/api/finance/mpesa_callback/

# Frontend URL
FRONTEND_URL=http://localhost:5173
```

#### 6. Run Database Migrations
```bash
python manage.py migrate
```

#### 7. Seed Initial Data
```bash
# Create departments
python manage.py seed_departments

# Create superuser (admin)
python manage.py create_superuser_auto
# Or manually:
# python manage.py createsuperuser
```

#### 8. Verify Setup
```bash
python manage.py check
```

---

### Frontend Setup

#### 1. Navigate to Frontend Directory
```bash
cd ../FRONTEND
```

#### 2. Install Node Dependencies
```bash
npm install
```

#### 3. Configure Environment Variables
Create a `.env` file in the `FRONTEND` directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## Configuration

### Django Admin Configuration
The Django admin panel provides a powerful interface for managing system data:
- **URL**: http://localhost:8000/admin/
- **Default credentials**: 
  - Email: `admin@mksu.ac.ke`
  - Password: `admin123456` (change immediately in production)

### Cache Configuration (Optional)
For production, configure Redis caching in `config/settings.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/0',
    }
}
```

For development without Redis, use local memory cache:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

---

## Running the Application

### Start Backend Server
```bash
cd BACKEND
python manage.py runserver
```
Backend will be available at: http://localhost:8000

### Start Frontend Development Server
```bash
cd FRONTEND
npm run dev
```
Frontend will be available at: http://localhost:5173

### Access API Documentation
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

---

## API Documentation

### Authentication
All API endpoints (except auth) require JWT authentication:

```bash
# Login
POST /api/auth/login/
Body: { "email": "user@example.com", "password": "password" }
Response: { "access": "token", "refresh": "token" }

# Use token in headers
Authorization: Bearer <access_token>
```

### Key Endpoints

#### Students
- `GET /api/students/` - List all students
- `POST /api/students/` - Create student (admin only)
- `GET /api/students/{id}/` - Student details
- `GET /api/students/me/` - Current student's profile
- `GET /api/students/eligible/` - Eligible students

#### Clearances
- `GET /api/clearances/` - List clearance requests
- `POST /api/clearances/` - Submit clearance request
- `GET /api/clearances/{id}/` - Clearance details
- `POST /api/clearances/{id}/submit/` - Submit request

#### Approvals
- `GET /api/approvals/` - List approvals
- `POST /api/approvals/{id}/process/` - Approve/reject clearance

#### Finance
- `GET /api/finance/payments/` - List payments
- `POST /api/finance/payments/` - Record payment
- `POST /api/finance/payments/{id}/verify/` - Verify payment

#### Gown Issuance
- `GET /api/gown-issuances/` - List gown issuances
- `POST /api/gown-issuances/` - Issue gown
- `POST /api/gown-issuances/{id}/mark_returned/` - Mark returned
- `GET /api/gown-issuances/overdue/` - Overdue returns
- `GET /api/gown-issuances/statistics/` - Statistics

#### Analytics
- `GET /api/analytics/dashboard/` - Overall dashboard
- `GET /api/analytics/clearance-completion/` - Completion rates
- `GET /api/analytics/department-bottlenecks/` - Bottleneck analysis
- `GET /api/analytics/financial-summary/` - Financial reports

#### Academics
- `GET /api/academics/schools/` - List schools
- `GET /api/academics/departments/` - List academic departments
- `GET /api/academics/courses/` - List courses

For complete API documentation with request/response examples, visit the Swagger UI at http://localhost:8000/api/docs/

---

## Usage Guide

### For Students

1. **Register/Login**: Create account or login with credentials
2. **Complete Profile**: Ensure registration number follows format `SCHOOL/DEPT/NNNN/YYYY`
3. **Submit Clearance**: Navigate to clearance page and submit request
4. **Upload Documents**: Attach required evidence files (max 5MB)
5. **Pay Graduation Fee**: Pay exactly KES 10,000 via M-PESA
6. **Track Progress**: Monitor approval status across departments
7. **Collect Gown**: Once approved, proceed to gown issuance

### For Department Staff

1. **Login**: Use department staff credentials
2. **View Pending**: Access department dashboard for pending approvals
3. **Review Requests**: Check student details and uploaded evidence
4. **Approve/Reject**: Make decision with notes or rejection reason
5. **Upload Evidence**: Attach department-specific documents if needed

### For Administrators

1. **Login to Admin Panel**: http://localhost:8000/admin/
2. **Manage Users**: Create students, staff, and admin accounts
3. **Configure Departments**: Set approval order and active status
4. **Manage Academic Structure**: Add schools, departments, courses
5. **Verify Payments**: Review and verify student payments
6. **Track Gown Issuance**: Manage gown assignments and returns
7. **View Analytics**: Access dashboards for system insights
8. **Review Audit Logs**: Monitor system activity and compliance

---

## Troubleshooting

### Backend Issues

#### Database Connection Error
```
Error: django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")
```
**Solution**:
1. Ensure MySQL server is running: `mysql --version`
2. Verify database credentials in `.env` file
3. Check database exists: `SHOW DATABASES;` in MySQL
4. Ensure user has proper permissions

#### Migration Errors
```
Error: No migrations to apply
```
**Solution**:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Redis Connection Error (Throttling)
```
Error: ConnectionRefusedError: [Errno 111] Connection refused
```
**Solution**:
- **Option 1**: Install and start Redis server
- **Option 2**: Switch to local memory cache in `settings.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

#### Import Errors
```
Error: ModuleNotFoundError: No module named 'rest_framework'
```
**Solution**:
```bash
pip install -r requirements.txt
```

### Frontend Issues

#### Module Not Found
```
Error: Cannot find module 'axios'
```
**Solution**:
```bash
npm install
```

#### CORS Errors
```
Error: Access to XMLHttpRequest blocked by CORS policy
```
**Solution**:
- Ensure backend `CORS_ALLOWED_ORIGINS` includes frontend URL in `settings.py`
- Update `.env` with correct `FRONTEND_URL`

#### Port Already in Use
```
Error: Port 5173 is already in use
```
**Solution**:
```bash
# Use different port
npm run dev -- --port 3000

# Or kill process using the port (Windows)
netstat -ano | findstr :5173
taskkill /PID <pid> /F
```

### General Issues

#### File Upload Fails
```
Error: File size exceeds maximum allowed size
```
**Solution**:
- Evidence files: Maximum 5MB
- Fee statements: Maximum 5MB
- Check file format is supported

#### Registration Number Validation
```
Error: Registration number must follow format SCHOOL/DEPT/NNNN/YYYY
```
**Solution**:
- Ensure format: `SCE/CS/0001/2024`
- School and department codes must be uppercase
- Sequence must be 4 digits
- Year must be 4 digits

#### Payment Amount Validation
```
Error: Payment amount must be exactly KES 10,000
```
**Solution**:
- Graduation fee is fixed at KES 10,000.00
- Do not modify the amount in the payment form

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Use ESLint/Prettier for JavaScript code formatting
- Write unit tests for new features
- Update API documentation when adding endpoints
- Maintain backward compatibility

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

For issues, questions, or contributions:
- **Issues**: https://github.com/yourusername/MksU-Clearance-System/issues
- **Email**: support@mksu.ac.ke
- **Documentation**: http://localhost:8000/api/docs/

---

## Acknowledgments

- Machakos University ICT Department
- All contributors and testers
- Django and React communities

---

**Built with ❤️ for Machakos University**