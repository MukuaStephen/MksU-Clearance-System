@echo off
REM Database setup script for MksU Clearance System (Windows)
REM Run after initial git clone to set up the development database

echo.
echo 🚀 MksU Clearance System - Database Setup
echo ==========================================
echo.

REM Check if Python virtual environment exists
if not exist "venv" (
    echo ⚠️  Virtual environment not found. Create it with:
    echo    python -m venv venv
    echo    venv\Scripts\activate
    exit /b 1
)

REM Check if environment variables are set
if not exist ".env" (
    echo ⚠️  .env file not found. Please copy .env.example to .env and update values.
    exit /b 1
)

echo ✓ Checking environment setup...
echo.

REM Run makemigrations
echo 📋 Step 1: Creating migrations...
python manage.py makemigrations
echo ✓ Migrations created
echo.

REM Run migrate
echo 💾 Step 2: Applying migrations to database...
python manage.py migrate
echo ✓ Database tables created
echo.

REM Seed departments
echo 🏢 Step 3: Seeding department data...
python manage.py seed_departments
echo.

REM Create superuser
echo 👤 Step 4: Creating superuser account...
echo Enter superuser details:
python manage.py createsuperuser
echo.

REM Collect static files (if needed)
echo 📦 Step 5: Collecting static files...
python manage.py collectstatic --noinput
echo ✓ Static files collected
echo.

REM Run tests
echo 🧪 Step 6: Running initial tests...
python manage.py test apps --verbosity=2
echo.

echo ✅ Database setup complete!
echo.
echo Next steps:
echo 1. Start the development server: python manage.py runserver
echo 2. Access Django admin: http://localhost:8000/admin/
echo 3. Login with superuser credentials you just created
echo.
pause
