# Quick Start Guide - Machakos Clearance Backend

## Step 1: Set Up Python Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Configure Environment Variables

1. Copy `.env.example` to `.env`
```bash
cp .env.example .env
```

2. Edit `.env` file with your configuration:
   - Set `SECRET_KEY` to a strong random string
   - Configure MySQL database connection
   - Set `FRONTEND_URL` to `http://localhost:5173`
   - Add email configuration if needed

## Step 4: Create MySQL Database

```sql
CREATE DATABASE machakos_clearance CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 6: Create Superuser (Admin)

```bash
python manage.py createsuperuser
# Follow prompts to create admin user
```

## Step 7: Run Development Server

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

## Step 8: Access Django Admin

Go to `http://localhost:8000/admin` and log in with your superuser credentials.

## Health Check

Test the API with:
```bash
curl http://localhost:8000/api/health/
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Machakos Clearance System API"
}
```

## Useful Commands

```bash
# Create new migration
python manage.py makemigrations apps.app_name

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server with auto-reload
python manage.py runserver

# Run tests
pytest

# Collect static files
python manage.py collectstatic

# Format code with black
black apps/

# Lint code with flake8
flake8 apps/

# Interactive shell
python manage.py shell
```

## Project Structure

```
BACKEND/
├── config/              # Django configuration
├── apps/                # Django applications
│   ├── users/          # User management & auth
│   ├── students/       # Student data
│   ├── departments/    # Department management
│   ├── clearances/     # Clearance requests
│   ├── approvals/      # Approval workflow
│   ├── finance/        # Finance verification
│   ├── notifications/  # Email/SMS alerts
│   └── audit_logs/     # Audit logging
├── manage.py           # Django management script
├── requirements.txt    # Dependencies
├── .env               # Environment variables (gitignored)
└── README.md          # Full documentation
```

## Next Steps

1. **Create Database Models** - Define User, Student, Department, Clearance models
2. **Implement Authentication** - JWT authentication and role-based access control
3. **Build API Endpoints** - RESTful endpoints for all features
4. **Add Business Logic** - Clearance workflow, approval routing
5. **Integrate Notifications** - Email alerts for status changes
6. **Write Tests** - Unit and integration tests

## Troubleshooting

### Database Connection Error
- Check MySQL is running
- Verify credentials in `.env`
- Ensure database exists: `CREATE DATABASE machakos_clearance;`

### Module Not Found
- Activate virtual environment
- Run `pip install -r requirements.txt`

### Migration Errors
- Delete migrations in app directories (except initial)
- Delete database
- Run `python manage.py makemigrations`
- Run `python manage.py migrate`

## Need Help?

Refer to:
- `README.md` for comprehensive documentation
- `project-plan-and-roles.md` for project scope
- Django docs: https://docs.djangoproject.com/
- DRF docs: https://www.django-rest-framework.org/
