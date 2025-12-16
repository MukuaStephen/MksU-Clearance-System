from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from apps.users.models import User
from apps.audit_logs.models import AuditLog

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class AuditLogsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@mksu.ac.ke',
            password='admin123456',
            full_name='Admin User',
            role='admin'
        )
        self.client.force_authenticate(user=self.admin)

    def test_health_check_is_logged(self):
        # Hit health endpoint (should be under /api/health/ and logged)
        res = self.client.get('/api/health/')
        self.assertEqual(res.status_code, 200)
        # Verify an audit log exists with entity='/api/health/'
        logs = AuditLog.objects.filter(entity='/api/health/')
        self.assertGreaterEqual(logs.count(), 1)
        entry = logs.first()
        self.assertEqual(entry.action, 'other')
        self.assertEqual(str(entry.entity_id), '200')
        self.assertIsNotNone(entry.changes)

    def test_audit_logs_api_admin_only(self):
        # List audit logs as admin
        res = self.client.get('/api/audit-logs/')
        self.assertEqual(res.status_code, 200)
        # Create a non-admin user and try access
        student = User.objects.create_user(
            username='student',
            email='student@mksu.ac.ke',
            password='student123456',
            full_name='Student User',
            role='student'
        )
        self.client.force_authenticate(user=student)
        res2 = self.client.get('/api/audit-logs/')
        self.assertEqual(res2.status_code, 403)
