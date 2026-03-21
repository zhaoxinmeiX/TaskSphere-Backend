from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class TaskModelTest(TestCase):
    """Test basic Task model functionality"""
    
    def test_task_creation(self):
        """Test that we can create a task"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        from .models import Task
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            user=user
        )
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.user, user)
        self.assertIsNotNone(task.id)


class TaskAPITest(APITestCase):
    """Test Task API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_task_list_endpoint(self):
        """Test that task list endpoint works"""
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_task_create_endpoint(self):
        """Test that task creation endpoint works"""
        data = {
            'title': 'New Task',
            'description': 'Task description'
        }
        response = self.client.post('/api/tasks/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_task_update_endpoint(self):
        """Test that task update endpoint works for title, description, and status"""
        # First create a task
        from .models import Task
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            user=self.user
        )
        
        # Test updating title and description
        data = {
            'title': 'Updated Task Title',
            'description': 'Updated Task Description'
        }
        response = self.client.patch(f'/api/tasks/{task.id}/update/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task Title')
        self.assertEqual(response.data['description'], 'Updated Task Description')
        
        # Test updating status
        data = {'status': 'completed'}
        response = self.client.patch(f'/api/tasks/{task.id}/update/', data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')
        
        # Verify database was updated
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task Title')
        self.assertEqual(task.description, 'Updated Task Description')
        self.assertEqual(task.status, 'completed')
