from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Task


class TaskStatusUpdateTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='todo',
            user=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_update_task_status(self):
        """Test updating task status via API"""
        url = f'/api/tasks/{self.task.id}/update/'
        data = {'status': 'in_progress'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'in_progress')

    def test_update_task_status_to_completed(self):
        """Test updating task status to completed"""
        url = f'/api/tasks/{self.task.id}/update/'
        data = {'status': 'completed'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'completed')

    def test_update_task_status_invalid_value(self):
        """Test updating task status with invalid value"""
        url = f'/api/tasks/{self.task.id}/update/'
        data = {'status': 'invalid_status'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_task_status_missing_field(self):
        """Test updating task without status field"""
        url = f'/api/tasks/{self.task.id}/update/'
        data = {'title': 'Updated Title'}
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Status field is required')
