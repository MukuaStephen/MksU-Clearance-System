#!/bin/bash
# Database setup script for MksU Clearance System
# Run after initial git clone to set up the development database

set -e  # Exit on first error

echo "🚀 MksU Clearance System - Database Setup"
echo "=========================================="
echo ""

# Check if Python virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Create it with:"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"
    exit 1
fi

# Check if environment variables are set
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Please copy .env.example to .env and update values."
    exit 1
fi

echo "✓ Checking environment setup..."
echo ""

# Run makemigrations
echo "📋 Step 1: Creating migrations..."
python manage.py makemigrations
echo "✓ Migrations created"
echo ""

# Run migrate
echo "💾 Step 2: Applying migrations to database..."
python manage.py migrate
echo "✓ Database tables created"
echo ""

# Seed departments
echo "🏢 Step 3: Seeding department data..."
python manage.py seed_departments
echo ""

# Create superuser
echo "👤 Step 4: Creating superuser account..."
echo "Enter superuser details:"
python manage.py createsuperuser
echo ""

# Collect static files (if needed)
echo "📦 Step 5: Collecting static files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected"
echo ""

# Run tests
echo "🧪 Step 6: Running initial tests..."
python manage.py test apps --verbosity=2
echo ""

echo "✅ Database setup complete!"
echo ""
echo "Next steps:"
echo "1. Start the development server: python manage.py runserver"
echo "2. Access Django admin: http://localhost:8000/admin/"
echo "3. Login with superuser credentials you just created"
echo ""
