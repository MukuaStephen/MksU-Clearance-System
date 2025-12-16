# Quick Access Guide - MksU Clearance System Backend

## Development Environment Status

✅ **Backend Server:** Running on http://localhost:8000/  
✅ **Database:** MySQL (mksu_clearance)  
✅ **Frontend Server:** Running on http://localhost:5173/  

---

## Admin Dashboard Access

### URL
```
http://localhost:8000/admin/
```

### Credentials
```
Email: admin@mksu.ac.ke
Password: admin123456
```

### Available Admin Interfaces
- **Users** - View/manage system users, admins, department staff, students
- **Students** - Manage student profiles and academic information
- **Departments** - Manage departments and their approval ordering
- **Clearance Requests** - View clearance submissions and track progress
- **Approvals** - View and manage department approvals
- **Finance Records** - View payment status and M-PESA verification
- **Notifications** - View notification history
- **Audit Logs** - View system action audit trail (read-only)

---

## Start/Stop Commands

### Start Backend Server
```bash
cd BACKEND
python manage.py runserver
```
- Accessible at: http://localhost:8000/
- Admin at: http://localhost:8000/admin/
- Auto-reloads on file changes

### Start Frontend Server
```bash
cd FRONTEND
npm run dev
```
- Accessible at: http://localhost:5173/
- Auto-compiles on file changes

### Stop Servers
- Backend: Press `CTRL+BREAK` in terminal
- Frontend: Press `CTRL+C` in terminal

---

## Database Management

### View Database (Admin Interface)
```
http://localhost:8000/admin/
```

### Switch to MySQL (Development)
1. Ensure MySQL Server is running locally (port 3306).
2. Create a database:
```sql
CREATE DATABASE mksu_clearance CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
3. Copy `BACKEND/.env.mysql.example` to `BACKEND/.env` and set your credentials.
4. Install Python deps (already present): `mysqlclient` or `PyMySQL`.
    - This project auto-enables `PyMySQL` as a MySQLdb shim.
5. Apply migrations:
```bash
cd BACKEND
python manage.py migrate
```

### Database Backup
```bash
cd BACKEND
python manage.py dumpdata > backup_$(date +%Y%m%d).json
```

### Database Reset (Development Only!)
```bash
cd BACKEND
python manage.py flush          # Delete all data
python manage.py migrate        # Re-create tables (uses MySQL if configured in .env)
python manage.py seed_departments
python manage.py create_superuser_auto
```

---

## Database Schema Summary

| Table | Purpose | Records |
|-------|---------|---------|
| users_user | User authentication (Admin, Staff, Students) | 1 (admin) |
| students_student | Student profiles | 0 (to be created) |
| departments_department | Clearance approval departments | 8 (seeded) |
| clearances_clearancerequest | Clearance requests | 0 (to be created) |
| approvals_clearanceapproval | Department approvals in workflow | 0 (to be created) |
| finance_financerecord | Payment tracking | 0 (to be created) |
| notifications_notification | System notifications | 0 (to be created) |
| audit_logs_auditlog | Action audit trail | (auto-logged) |

---

## 8-Department Clearance Workflow

Clearances route through departments in this order:

1. **Finance Department** - Verify tuition/graduation fee payment
2. **Library Services** - Verify book returns
3. **Mess/Cafeteria** - Verify meal plan settlement
4. **Hostel Office** - Verify room clearance
5. **Academic Affairs** - Release grades and final transcript
6. **Workshop/Laboratories** - Verify equipment returns
7. **Sports & Games** - Verify sports clearance
8. **Student Services** - Final compliance checks

---

## File Structure

```
MksU-Clearance-System/
├── FRONTEND/                  # React/Vite frontend
│   ├── src/
│   │   ├── App.jsx
│   │   ├── pages/
│   │   └── components/
│   └── package.json
│
└── BACKEND/                   # Django REST API
    ├── config/                # Django settings & URLs
    │   ├── settings.py        # Configuration (SQLite, JWT, CORS, etc.)
    │   ├── urls.py            # API routing
    │   └── wsgi.py            # WSGI application
    │
    ├── apps/                  # Django applications (8 apps)
    │   ├── users/             # User authentication & roles
    │   ├── students/          # Student profiles
    │   ├── departments/       # Department management
    │   ├── clearances/        # Clearance requests
    │   ├── approvals/         # Approval workflow
    │   ├── finance/           # Payment tracking
    │   ├── notifications/     # In-app notifications
    │   └── audit_logs/        # System audit trail
    │
    ├── manage.py              # Django CLI
    ├── requirements.txt       # Python dependencies
    ├── .env                   # Environment variables (SQLite config)
    ├── db.sqlite3             # Development database
    │
    ├── MIGRATIONS_GUIDE.md       # Database setup guide
    ├── TASK3_COMPLETION_REPORT.md
    ├── README.md              # Backend setup instructions
    └── QUICKSTART.md          # Quick reference guide
```

---

## Common Tasks

### Create a Test Student
```bash
cd BACKEND
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> from apps.students.models import Student
>>> User = get_user_model()
>>> user = User.objects.create_user(
...     email='student@mksu.ac.ke',
...     admission_number='ADM001',
...     full_name='John Doe',
...     password='password123',
...     role='student'
... )
>>> student = Student.objects.create(
...     user=user,
...     registration_number='REG001',
...     faculty='Engineering',
...     program='Software Engineering',
...     graduation_year=2024,
...     eligibility_status='eligible'
... )
>>> exit()
```

### View All Departments
```bash
cd BACKEND
python manage.py shell
>>> from apps.departments.models import Department
>>> for dept in Department.objects.all().order_by('approval_order'):
...     print(f"{dept.approval_order}. {dept.name} ({dept.code})")
```

### Create a Clearance Request
Via admin panel: http://localhost:8000/admin/clearances/clearancerequest/add/

---

## Key URLs

| URL | Purpose | Auth Required |
|-----|---------|---------------|
| `http://localhost:8000/` | API Root | No |
| `http://localhost:8000/admin/` | Django Admin | Yes (admin) |
| `http://localhost:8000/api/` | API Base | Yes (JWT) |
| `http://localhost:5173/` | Frontend | No |

### API Documentation
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- Raw OpenAPI schema: `http://localhost:8000/api/schema/`
- Authorize with JWT via the lock/Authorize button (Bearer token).

---

## Important Notes

### Default Admin Password
⚠️ **IMPORTANT:** Change the default password immediately!

```
Current: admin123456
Change in Django Admin after first login
```

### Environment Variables (.env)
```
DEBUG=True                      # Enable debug mode (dev only)
SECRET_KEY=...                  # Django secret key
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

### Frontend-Backend Communication
- Frontend: http://localhost:5173/
- Backend: http://localhost:8000/
- CORS: Configured to allow localhost:5173 → localhost:8000

---

## Troubleshooting

### Server Won't Start
```bash
# Check for syntax errors
python manage.py check

# Check if port is already in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Mac/Linux

# Try different port
python manage.py runserver 8001
```

### Database Issues (MySQL)
```sql
-- Reset database completely (destructive!)
DROP DATABASE IF EXISTS mksu_clearance;
CREATE DATABASE mksu_clearance CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
```bash
cd BACKEND
python manage.py migrate
python manage.py seed_departments
python manage.py create_superuser_auto
```

### Admin Panel Not Loading
- Clear browser cache
- Check if Django admin is registered in INSTALLED_APPS
- Run: `python manage.py check`

---

## Contact & Support

For issues or questions:
1. Check documentation in BACKEND/ folder
2. Review Django logs in console output
3. Check database integrity in Django admin

---

## Audit Logs

### Overview
- Records API activity and important actions (create, update, delete, approve, reject).
- Admin-only read access; pagination enabled by default (20 per page).

### Endpoints
- List: `GET /api/audit-logs/`
- Detail: `GET /api/audit-logs/{id}/`
- Statistics: `GET /api/audit-logs/statistics/`
- Recent: `GET /api/audit-logs/recent/`
- By User: `GET /api/audit-logs/by_user/?user={uuid}`

### Filters
- Action: `?action=create|update|delete|approve|reject|other`
- Entity contains: `?contains=/api/clearances` (matches path/entity substrings)
- Timestamp window (UTC):
    - DateTime range: `?start=2025-12-01T00:00:00Z&end=2025-12-16T23:59:59Z`
    - Date-only range: `?date_start=2025-12-01&date_end=2025-12-16` (uses `created_at__date`)
- Ordering: `?ordering=-created_at` (default), or `?ordering=action`

### Pagination
- Default page size: `20`
- Page param: `?page=1`

### Examples
```bash
# List latest logs (page 1)
curl -H "Authorization: Bearer <JWT>" \
    http://localhost:8000/api/audit-logs/

# Filter by action and date-only window
curl -H "Authorization: Bearer <JWT>" \
    "http://localhost:8000/api/audit-logs/?action=create&date_start=2025-12-01&date_end=2025-12-16&ordering=-created_at&page=1"

# Statistics summary
curl -H "Authorization: Bearer <JWT>" \
    http://localhost:8000/api/audit-logs/statistics/

# Recent top 20 entries
curl -H "Authorization: Bearer <JWT>" \
    http://localhost:8000/api/audit-logs/recent/
```

---

**Last Updated:** December 16, 2025  
**Status:** ✅ Backend Ready for API Development  
**Next Phase:** Task 4 - User Authentication System
