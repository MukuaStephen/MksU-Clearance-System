#!/usr/bin/env python
"""
Create test users for the MksU Clearance System
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

def create_test_users():
    """Create admin, staff, and student test users"""
    
    # Create or Update Admin User
    admin, created = User.objects.get_or_create(
        email='admin@mksu.ac.ke',
        defaults={
            'username': 'admin@mksu.ac.ke',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True
        }
    )
    admin.set_password('admin123')
    admin.save()
    print(f'✓ {"Created" if created else "Updated"} admin user: {admin.email}')

    # Create or Update Department Staff User
    staff, created = User.objects.get_or_create(
        email='staff@mksu.ac.ke',
        defaults={
            'username': 'staff@mksu.ac.ke',
            'first_name': 'Department',
            'last_name': 'Staff',
            'role': 'department_staff'
        }
    )
    staff.set_password('staff123')
    staff.save()
    print(f'✓ {"Created" if created else "Updated"} staff user: {staff.email}')

    # Create or Update Student User
    student, created = User.objects.get_or_create(
        email='student@example.com',
        defaults={
            'username': 'student@example.com',
            'first_name': 'Test',
            'last_name': 'Student',
            'role': 'student'
        }
    )
    student.set_password('password123')
    student.save()
    print(f'✓ {"Created" if created else "Updated"} student user: {student.email}')

    print('\n✅ Test users setup complete!')
    print('\nLogin Credentials:')
    print('=' * 50)
    print('Admin:')
    print('  Email: admin@mksu.ac.ke')
    print('  Password: admin123')
    print('\nStaff:')
    print('  Email: staff@mksu.ac.ke')
    print('  Password: staff123')
    print('\nStudent:')
    print('  Email: student@example.com')
    print('  Password: password123')
    print('=' * 50)

if __name__ == '__main__':
    create_test_users()
