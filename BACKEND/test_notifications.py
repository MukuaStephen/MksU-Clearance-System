import json
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from apps.users.models import User
from apps.notifications.models import Notification


@override_settings(CACHES={
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
})
class NotificationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@mksu.ac.ke',
            password='admin123456',
            full_name='Admin User',
            role='admin'
        )
        self.student = User.objects.create_user(
            username='student',
            email='student@mksu.ac.ke',
            password='student123456',
            full_name='Student User',
            role='student'
        )
        # Authenticate as admin directly
        self.client.force_authenticate(user=self.admin)

    def test_create_and_list_notifications(self):
        # Create notification for student
        res = self.client.post('/api/notifications/', {
            'recipient_id': str(self.student.id),
            'notification_type': 'general',
            'title': 'Test Notice',
            'message': 'Hello world'
        }, format='json')
        self.assertEqual(res.status_code, 201, msg=res.content)
        notif_id = res.data.get('id')
        self.assertTrue(notif_id)
        
        # Switch to student
        self.client.force_authenticate(user=self.student)
        
        # List my notifications
        res = self.client.get('/api/notifications/')
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)
        
        # Mark as read
        res = self.client.post(f'/api/notifications/{notif_id}/mark_as_read/')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data['notification']['is_read'])
        
        # Unread count
        res = self.client.get('/api/notifications/unread_count/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['unread_count'], 0)
