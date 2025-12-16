"""
Django management command to create initial superuser.
Usage: python manage.py create_superuser_auto
"""
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from apps.users.models import User


class Command(BaseCommand):
    help = 'Create initial superuser account for system administration'

    def handle(self, *args, **options):
        """Create superuser if it doesn't already exist."""
        
        email = 'admin@mksu.ac.ke'
        admission_number = 'ADMIN001'
        full_name = 'System Administrator'
        password = 'admin123456'
        
        try:
            if User.objects.filter(email=email).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f'⊘ Superuser already exists: {email}'
                    )
                )
            else:
                user = User.objects.create_superuser(
                    email=email,
                    admission_number=admission_number,
                    full_name=full_name,
                    password=password,
                    username=email  # Use email as username
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Superuser created successfully!'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  Email: {user.email}'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  Full Name: {user.full_name}'
                    )
                )
                self.stdout.write(
                    self.style.WARNING(
                        f'\n⚠️  Default password: {password}'
                    )
                )
                self.stdout.write(
                    self.style.WARNING(
                        f'   Please change this password immediately after first login!'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n📍 Access Django admin at: http://localhost:8000/admin/'
                    )
                )
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(
                    f'✗ Error creating superuser: {str(e)}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'✗ Unexpected error: {str(e)}'
                )
            )
