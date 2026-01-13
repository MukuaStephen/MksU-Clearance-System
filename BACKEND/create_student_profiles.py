#!/usr/bin/env python
"""
Create Student profiles for users with role='student'
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.students.models import Student

def create_student_profiles():
    """Create Student profiles for users with role='student' who don't have one"""
    
    student_users = User.objects.filter(role='student')
    created_count = 0
    
    for user in student_users:
        # Check if student profile already exists
        if hasattr(user, 'student_profile'):
            print(f'  Student profile already exists for: {user.email}')
            continue
        
        # Extract registration number from admission number or create one
        reg_number = user.admission_number if user.admission_number else f'SCE/CS/{str(user.id)[:4].upper()}/2024'
        
        # Create student profile
        from apps.students.models import Student
        student = Student.objects.create(
            user=user,
            registration_number=reg_number,
            faculty='School of Computing and Engineering',
            program='Bachelor of Science in Computer Science',
            graduation_year=2026,
            eligibility_status='eligible'
        )
        print(f'✓ Created student profile for: {user.email}')
    
    print('\n✅ Student profiles setup complete!')

if __name__ == '__main__':
    create_student_profiles()
