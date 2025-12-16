# Machakos University Clearance System - Backend API

This is the backend API for the Machakos University Graduation Clearance System built with **Django** and **MySQL**. It handles student applications, payments, and departmental clearances.

## Technology Stack

- **Framework:** Django 4.2.7
- **API:** Django REST Framework
- **Database:** MySQL
- **Authentication:** JWT
- **Cache:** Redis
- **Task Queue:** Celery
- **Python:** 3.8+

## Project Structure

```
BACKEND/
├── config/              # Django configuration
│   ├── settings.py      # Project settings
│   ├── urls.py          # URL routing
│   ├── wsgi.py          # WSGI configuration
│   └── __init__.py
├── apps/                # Django applications
│   ├── users/           # User management & authentication
│   ├── students/        # Student data & profiles
│   ├── departments/     # Department management
│   ├── clearances/      # Clearance requests & tracking
│   ├── approvals/       # Clearance approvals workflow
│   ├── finance/         # Finance verification & fees
│   ├── notifications/   # Email/SMS notifications
│   └── audit_logs/      # Audit trail logging
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── .env.example         # Environment variables template
└── README.md
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)
- Redis (optional, for caching and task queue)

### 1. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and update with your values:

```bash
cp .env.example .env
```

Update the following in `.env`:
- `SECRET_KEY` - Generate a strong Django secret key
- `DB_NAME`, `DB_USER`, `DB_PASSWORD` - MySQL credentials
- `FRONTEND_URL` - Frontend application URL
- `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` - Email configuration

### 4. Create MySQL Database

```sql
CREATE DATABASE machakos_clearance CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Server will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user
- `POST /api/auth/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### Students
- `GET /api/students/` - List all students
- `POST /api/students/` - Create new student
- `GET /api/students/{id}/` - Get student details
- `PUT /api/students/{id}/` - Update student

### Departments
- `GET /api/departments/` - List all departments
- `POST /api/departments/` - Create department
- `GET /api/departments/{id}/` - Get department details

### Clearances
- `GET /api/clearances/` - List clearance requests
- `POST /api/clearances/` - Create clearance request
- `GET /api/clearances/{id}/` - Get clearance details
- `PUT /api/clearances/{id}/` - Update clearance status

### Approvals
- `GET /api/approvals/` - List approvals
- `POST /api/approvals/` - Approve/reject clearance
- `GET /api/approvals/{id}/` - Get approval details

### Finance
- `GET /api/finance/students/{id}/` - Get student finance record
- `POST /api/finance/verify/` - Verify graduation fee payment

### Notifications
- `GET /api/notifications/` - List user notifications
- `PUT /api/notifications/{id}/mark-read/` - Mark notification as read

### Audit Logs
- `GET /api/audit-logs/` - List audit logs (admin only)

## Core Data Models

### User
- id (UUID)
- email (unique)
- admission_number
- full_name
- role (admin, department_staff, student)
- is_active
- last_login
- created_at
- updated_at

### Student
- id (UUID)
- user (FK to User)
- registration_number (unique)
- faculty
- program
- graduation_year
- eligibility_status

### Department
- id (UUID)
- name (Finance, Library, Mess, Hostel, etc.)
- code
- head_email
- type (finance, academic, residential, etc.)

### ClearanceRequest
- id (UUID)
- student (FK to Student)
- status (pending, in_progress, completed, rejected)
- submission_date
- completion_date
- created_at
- updated_at

### ClearanceApproval
- id (UUID)
- clearance_request (FK to ClearanceRequest)
- department (FK to Department)
- status (pending, approved, rejected)
- approved_by (FK to User)
- approval_date
- rejection_reason
- notes

### FinanceRecord
- id (UUID)
- student (FK to Student)
- tuition_balance
- graduation_fee_status (pending, paid, verified)
- last_verified_date
- mpesa_code (M-PESA confirmation code)

### Notification
- id (UUID)
- user (FK to User)
- message
- type (approval, rejection, update, alert)
- read (boolean)
- created_at
- sent_at

### AuditLog
- id (UUID)
- actor (FK to User)
- action (create, update, delete, approve, reject)
- entity (model name)
- entity_id
- changes (JSON - before/after values)
- created_at
- ip_address

## Key Features

### 1. Authentication & Authorization
- SSO integration with university email/admission number
- JWT-based authentication
- Role-based access control (RBAC)
- Session management

### 2. Student Clearance Workflow
- Auto-filled application forms from student records
- Real-time clearance status tracking
- Multi-department approval routing
- Support for approvals, rejections, and notes

### 3. Departmental Management
- Department-specific dashboards
- Bulk approval/rejection operations
- Filtering and searching capabilities
- Performance metrics and reporting

### 4. Finance Integration
- Graduation fee verification
- M-PESA payment confirmation
- Automatic fee validation
- Finance report generation

### 5. Notifications
- Email notifications for status changes
- SMS alerts (optional)
- In-app notification center
- Notification preferences management

### 6. Audit & Compliance
- Comprehensive audit logging
- Change tracking (before/after values)
- User action history
- Compliance reporting

### 7. Security
- Input validation and sanitization
- Rate limiting on API endpoints
- CORS protection
- CSRF token validation
- SQL injection prevention
- XSS protection

## Development

### Code Style
- Follow PEP 8 style guide
- Use black for code formatting
- Use flake8 for linting

### Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=apps
```

### Database Migrations

Create new migration:
```bash
python manage.py makemigrations apps.app_name
```

Apply migrations:
```bash
python manage.py migrate
```

## Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker

```bash
docker build -t clearance-backend .
docker run -p 8000:8000 clearance-backend
```

### Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up SSL/TLS certificates
- [ ] Configure email service
- [ ] Set up database backups
- [ ] Configure Redis for caching
- [ ] Set up Celery for async tasks
- [ ] Configure monitoring and logging
- [ ] Run security checks (`python manage.py check --deploy`)

## Monitoring & Logging

Logs are written to:
- Console (development)
- `logs/clearance.log` (file)

Log levels can be configured in `config/settings.py`

## Support & Documentation

- Django Docs: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Project Plan: See `project-plan-and-roles.md` in root

## License

Proprietary - Machakos University
