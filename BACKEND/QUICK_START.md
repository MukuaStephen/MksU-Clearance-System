# MksU Clearance System - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Setup Virtual Environment (First Time Only)
```powershell
cd BACKEND
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 2: Initialize Database (First Time Only)
```powershell
python manage.py migrate
python manage.py createsuperuser  # Optional: Create admin account
```

### Step 3: Start the Server
```powershell
# Easy way - use the startup script
.\start_server.ps1

# OR manual way
$env:DB_ENGINE="sqlite"
python manage.py runserver 8000
```

---

## 📍 Access Points

Once the server is running, you can access:

| Resource | URL | Description |
|----------|-----|-------------|
| **API Documentation** | http://localhost:8000/api/docs/ | Interactive Swagger UI |
| **Alternative Docs** | http://localhost:8000/api/redoc/ | ReDoc documentation |
| **Health Check** | http://localhost:8000/api/health/ | Server status |
| **Admin Panel** | http://localhost:8000/admin/ | Django admin interface |
| **OpenAPI Schema** | http://localhost:8000/api/schema/ | Raw API schema (JSON) |

---

## 🧪 Test the API

### Quick Health Check
```powershell
curl http://localhost:8000/api/health/
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Machakos Clearance System API"
}
```

### Run Comprehensive Tests
```powershell
python test_all_endpoints.py
```

### Manual Test (Register a User)
```powershell
curl -X POST http://localhost:8000/api/auth/register/ `
  -H "Content-Type: application/json" `
  -d '{
    "email":"student@mksu.ac.ke",
    "full_name":"John Doe",
    "admission_number":"SCE/CS/0001/2024",
    "password":"SecurePass123!",
    "password_confirm":"SecurePass123!",
    "role":"student"
  }'
```

---

## 📁 Project Structure

```
BACKEND/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── db.sqlite3            # SQLite database (development)
├── start_server.ps1      # Quick start script (PowerShell)
├── start_server.bat      # Quick start script (Batch)
├── test_all_endpoints.py # Comprehensive endpoint tests
│
├── config/               # Django configuration
│   ├── settings.py       # Main settings
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI application
│
├── apps/                 # Django applications
│   ├── users/           # Authentication & user management
│   ├── students/        # Student profiles
│   ├── departments/     # Department management
│   ├── clearances/      # Clearance requests
│   ├── approvals/       # Department approvals
│   ├── finance/         # Payments & finance
│   ├── notifications/   # Notification system
│   ├── gown_issuance/   # Gown tracking
│   ├── audit_logs/      # Audit trail
│   ├── academics/       # Academic structure
│   └── analytics/       # Reporting & analytics
│
└── venv/                # Virtual environment (created by you)
```

---

## 🔑 Key Features

### ✅ Complete API (90+ Endpoints)
- Authentication (JWT tokens)
- Student management
- Clearance workflow
- Department approvals
- Financial tracking
- Gown issuance
- Real-time notifications
- Audit logging
- Analytics & reporting

### ✅ Security
- JWT authentication
- Role-based access control (Student, Staff, Admin)
- CORS configuration
- Password hashing
- Token blacklisting
- Input validation

### ✅ Documentation
- Interactive Swagger UI
- ReDoc alternative
- OpenAPI 3.0 schema
- Code examples
- Request/response samples

---

## 🛠️ Common Commands

### Database Commands
```powershell
# Apply migrations
python manage.py migrate

# Create migrations after model changes
python manage.py makemigrations

# Create superuser for admin panel
python manage.py createsuperuser

# Reset database (CAUTION: Deletes all data!)
Remove-Item db.sqlite3
python manage.py migrate
```

### Development Commands
```powershell
# Start development server
python manage.py runserver 8000

# Run specific port
python manage.py runserver 9000

# Check for issues
python manage.py check

# Collect static files (production)
python manage.py collectstatic
```

### Testing Commands
```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest test_auth.py

# Run endpoint connectivity test
python test_all_endpoints.py
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the BACKEND directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DB_ENGINE=sqlite
SQLITE_DB_PATH=C:\path\to\BACKEND\db.sqlite3

# Database (MySQL for production)
# DB_ENGINE=mysql
# DB_NAME=mksu_clearance
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_HOST=localhost
# DB_PORT=3306

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=10080  # 7 days in minutes
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `QUICK_START.md` | This file - quick start guide |
| `ENDPOINT_VERIFICATION.md` | Complete endpoint list with verification |
| `BACKEND_API_SCHEMA.md` | Detailed API reference |
| `COMPLETE_BACKEND_SUMMARY.md` | Architecture overview |
| `FRONTEND_DEVELOPER_QUICK_REFERENCE.md` | Frontend integration guide |

---

## 🐛 Troubleshooting

### Server Won't Start
```powershell
# Check if port 8000 is in use
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess

# Kill process on port 8000
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess -Force

# Try a different port
python manage.py runserver 9000
```

### Database Errors
```powershell
# Reset migrations (CAUTION: Deletes all data!)
Remove-Item db.sqlite3
Remove-Item -Recurse -Force apps\*/migrations\0*.py
python manage.py makemigrations
python manage.py migrate
```

### Import Errors
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### CORS Errors
Check `config/settings.py` and ensure your frontend URL is in `CORS_ALLOWED_ORIGINS`.

---

## 🎯 Next Steps

1. **Start the Server**
   ```powershell
   .\start_server.ps1
   ```

2. **Test API Documentation**
   - Open http://localhost:8000/api/docs/
   - Try the interactive endpoints

3. **Create Test Data**
   - Use admin panel: http://localhost:8000/admin/
   - Or use API endpoints

4. **Frontend Integration**
   - Read `FRONTEND_DEVELOPER_QUICK_REFERENCE.md`
   - Use API base URL: `http://localhost:8000/api`

5. **Deploy to Production**
   - Switch to MySQL database
   - Set DEBUG=False
   - Configure Gunicorn + Nginx
   - Set up SSL/HTTPS

---

## 📞 Need Help?

- **API Documentation:** http://localhost:8000/api/docs/
- **Complete Endpoint List:** See `ENDPOINT_VERIFICATION.md`
- **Architecture Guide:** See `COMPLETE_BACKEND_SUMMARY.md`
- **Frontend Integration:** See `FRONTEND_DEVELOPER_QUICK_REFERENCE.md`

---

**Ready to go! 🚀**

Start the server with `.\start_server.ps1` and visit http://localhost:8000/api/docs/
