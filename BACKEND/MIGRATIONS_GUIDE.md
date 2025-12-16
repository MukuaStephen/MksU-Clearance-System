# Task 3: Database Migrations & Setup

Complete guide to initializing the database for MksU Clearance System.

## Prerequisites

- Virtual environment activated
- MySQL server running and accessible
- `.env` file properly configured with database credentials
- All Python dependencies installed (`pip install -r requirements.txt`)

## Step-by-Step Setup

### 1. Create Migrations

Generate migration files from model definitions:

```bash
python manage.py makemigrations
```

**What it does:**
- Detects changes in models since last migration
- Creates migration files in each app's `migrations/` folder
- Shows summary of changes detected

**Expected output:**
```
Migrations for 'users':
  0001_initial.py
    - Create model User
Migrations for 'students':
  0001_initial.py
    - Create model Student
...
```

### 2. Apply Migrations to Database

Execute all pending migrations against MySQL:

```bash
python manage.py migrate
```

**What it does:**
- Creates all database tables based on migrations
- Creates Django internal tables (auth, sessions, etc.)
- Marks migrations as applied in `django_migrations` table

**Expected output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, users, students, ...
Running migrations:
  Applying users.0001_initial... OK
  Applying students.0001_initial... OK
  Applying departments.0001_initial... OK
  ...
```

### 3. Seed Initial Department Data

Populate required department records for approval workflow:

```bash
python manage.py seed_departments
```

**What it does:**
- Creates 8 departments (Finance, Library, Mess, Hostel, Academic, Workshop, Sports, Student Services)
- Sets approval order (determines clearance routing sequence)
- Assigns department heads and contact emails

**Expected output:**
```
✓ Created department: Finance Department (Code: FINANCE)
✓ Created department: Library Services (Code: LIBRARY)
...
📊 Summary: 8 departments created, 0 skipped

📋 All Departments:
  1. Finance Department (FINANCE) - Order: 1 - ✓ Active
  2. Library Services (LIBRARY) - Order: 2 - ✓ Active
  ...
```

### 4. Create Superuser Account

Create admin user for Django admin interface:

```bash
python manage.py createsuperuser
```

**Interactive prompts:**
```
Email address: admin@makuni.ac.ke
Admission Number: ADMIN001
Full Name: System Administrator
Password: ••••••••••
Password (again): ••••••••••
Superuser created successfully.
```

**What it does:**
- Creates User with admin=True, staff=True, superuser=True
- Sets email and password
- Allows login to Django admin at `/admin/`

### 5. Test Database Connectivity

Verify database is properly set up:

```bash
python manage.py check
```

**Expected output:**
```
System check identified no issues (0 silenced).
```

### 6. Verify Tables Created

Open MySQL client and check tables:

```sql
use mku_clearance_dev;
SHOW TABLES;
```

**Expected tables:**
- `users_user` - Custom user model
- `students_student` - Student profiles
- `departments_department` - Departments for approval workflow
- `clearances_clearancerequest` - Clearance requests
- `approvals_clearanceapproval` - Department approvals
- `finance_financerecord` - Payment tracking
- `notifications_notification` - User notifications
- `audit_logs_auditlog` - System audit trail
- Plus Django's built-in tables: `auth_*`, `django_*`, `sessions_*`

**Count records:**
```sql
SELECT COUNT(*) FROM departments_department;  -- Should be 8
```

## Automated Setup Scripts

### Linux/Mac

```bash
chmod +x setup_db.sh
./setup_db.sh
```

### Windows

```cmd
setup_db.bat
```

**Script performs:**
1. Check virtual environment
2. Check .env file
3. Run makemigrations
4. Run migrate
5. Seed departments
6. Create superuser
7. Collect static files
8. Run tests

## Troubleshooting

### Migration Issues

**Error: "Cannot add a NOT NULL constraint on a field that doesn't have a default"**
- Model field changed from nullable to non-nullable
- Provide default value in migration: `--noinput` or `--default`

**Error: "Duplicate key value violates unique constraint"**
- Existing data conflicts with new unique constraint
- Manually fix data before migrating

### Database Connection Issues

**Error: "Access denied for user 'root'@'localhost'**
- Check `.env` file has correct MySQL credentials
- Verify MySQL server is running
- Test connection: `mysql -u root -p -h localhost`

**Error: "Unknown database 'mku_clearance_dev'"**
- Database doesn't exist
- Create manually: `CREATE DATABASE mku_clearance_dev;`
- Or update `.env` with existing database name

### Rollback Migrations

If migrations fail and need to rollback:

```bash
# Rollback all migrations for an app
python manage.py migrate departments zero

# Rollback specific migration
python manage.py migrate departments 0001

# List migration status
python manage.py showmigrations
```

## Database Schema

### User Roles
- **Admin**: Full system access
- **Department Staff**: Approve/reject clearances for assigned department
- **Student**: Submit clearance, view status

### Clearance Workflow
1. Student submits clearance request (after payment verified)
2. Request routed to Finance Department (first approval_order)
3. Finance approves/rejects
4. If approved, routes to Library (order 2)
5. Process continues through all 8 departments
6. Final approval sets status to "completed"

### Approval Sequence (approval_order)
1. Finance - Fee verification
2. Library - Book returns
3. Mess - Meal plan settlement
4. Hostel - Room clearance
5. Academic - Grade release, final transcript
6. Workshop - Equipment/material returns
7. Sports - Sports clearance
8. Student Services - General compliance

## Data Model Overview

```
User (Custom)
├── Student (OneToOne)
│   └── ClearanceRequest (ForeignKey)
│       ├── ClearanceApproval (ForeignKey) [8 per request, one per department]
│       │   ├── Department
│       │   └── User (approved_by)
│       └── FinanceRecord (OneToOne)
├── Notification (ForeignKey)
└── AuditLog (ForeignKey)
```

## Next Steps

After successful database setup:

1. **Start Development Server**
   ```bash
   python manage.py runserver
   ```
   - Backend API available at `http://localhost:8000/api/`
   - Django admin at `http://localhost:8000/admin/`

2. **Test API Endpoints** (see API Documentation)
   ```bash
   curl -X GET http://localhost:8000/api/departments/
   ```

3. **Create Test Data** (optional)
   ```bash
   python manage.py shell
   >>> from apps.students.models import Student
   >>> # Create test students
   ```

4. **Proceed to Task 4: Authentication System**
   - JWT token generation
   - Login/logout endpoints
   - Password hashing
   - Session management

## Database Maintenance

### Backup

```bash
python manage.py dumpdata > backup.json
```

### Restore

```bash
python manage.py loaddata backup.json
```

### Reset Database (Development Only!)

```bash
# Delete all data and re-migrate
python manage.py flush
python manage.py migrate
python manage.py seed_departments
```

## Command Reference

| Command | Purpose |
|---------|---------|
| `makemigrations` | Generate migration files from model changes |
| `migrate` | Apply migrations to database |
| `seed_departments` | Populate department records |
| `createsuperuser` | Create admin user |
| `check` | Verify Django setup |
| `showmigrations` | Display migration status |
| `flush` | Delete all data (dev only) |
| `shell` | Interactive Python shell with Django context |
| `dumpdata` | Export database to JSON |
| `loaddata` | Import data from JSON |

---

**Status:** Ready for API implementation after database verification ✅
**Next Task:** Task 4 - Implement User Authentication System
