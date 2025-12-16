"""
Django management command to seed initial department data.
Usage: python manage.py seed_departments
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from apps.departments.models import Department


class Command(BaseCommand):
    help = 'Seed initial department data for the clearance system'

    def handle(self, *args, **options):
        """Create initial departments required for the clearance workflow."""
        
        departments_data = [
            {
                'name': 'Finance Department',
                'code': 'FINANCE',
                'department_type': 'Finance',
                'head_email': 'finance.head@makuni.ac.ke',
                'approval_order': 1,
            },
            {
                'name': 'Library Services',
                'code': 'LIBRARY',
                'department_type': 'Library',
                'head_email': 'library.head@makuni.ac.ke',
                'approval_order': 2,
            },
            {
                'name': 'Mess/Cafeteria',
                'code': 'MESS',
                'department_type': 'Mess',
                'head_email': 'mess.manager@makuni.ac.ke',
                'approval_order': 3,
            },
            {
                'name': 'Hostel Office',
                'code': 'HOSTEL',
                'department_type': 'Hostel',
                'head_email': 'hostel.office@makuni.ac.ke',
                'approval_order': 4,
            },
            {
                'name': 'Academic Affairs',
                'code': 'ACADEMIC',
                'department_type': 'Faculty',
                'head_email': 'academic.dean@makuni.ac.ke',
                'approval_order': 5,
            },
            {
                'name': 'Workshop/Laboratories',
                'code': 'WORKSHOP',
                'department_type': 'Workshop',
                'head_email': 'workshop.head@makuni.ac.ke',
                'approval_order': 6,
            },
            {
                'name': 'Sports & Games',
                'code': 'SPORTS',
                'department_type': 'Sports',
                'head_email': 'sports.office@makuni.ac.ke',
                'approval_order': 7,
            },
            {
                'name': 'Student Services',
                'code': 'STUDENT_SERVICES',
                'department_type': 'Other',
                'head_email': 'student.services@makuni.ac.ke',
                'approval_order': 8,
            },
        ]
        
        created_count = 0
        skipped_count = 0

        for dept_data in departments_data:
            try:
                dept, created = Department.objects.get_or_create(
                    code=dept_data['code'],
                    defaults=dept_data
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Created department: {dept.name} (Code: {dept.code})'
                        )
                    )
                    created_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'⊘ Department already exists: {dept.name}'
                        )
                    )
                    skipped_count += 1
            except IntegrityError as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'✗ Error creating {dept_data["code"]}: {str(e)}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Summary: {created_count} departments created, {skipped_count} skipped'
            )
        )
        
        # Display all departments
        self.stdout.write('\n📋 All Departments:')
        all_depts = Department.objects.order_by('approval_order')
        for i, dept in enumerate(all_depts, 1):
            status = '✓ Active' if dept.is_active else '✗ Inactive'
            self.stdout.write(f'  {i}. {dept.name} ({dept.code}) - Order: {dept.approval_order} - {status}')
