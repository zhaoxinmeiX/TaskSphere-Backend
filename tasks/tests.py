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
    
    def test_task_delete_endpoint(self):
        """Test that task deletion endpoint works"""
        # First create a task
        from .models import Task
        task = Task.objects.create(
            title='Test Task to Delete',
            description='This task will be deleted',
            user=self.user
        )
        
        # Verify task exists
        self.assertTrue(Task.objects.filter(id=task.id).exists())
        
        # Delete the task
        response = self.client.delete(f'/api/tasks/{task.id}/delete/')
        
        # Check response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], 'Task deleted successfully')
        
        # Verify task is deleted from database
        self.assertFalse(Task.objects.filter(id=task.id).exists())
    
    def test_task_delete_unauthorized(self):
        """Test that unauthorized users cannot delete tasks"""
        # Create a task for the authenticated user
        from .models import Task
        task = Task.objects.create(
            title='User Task',
            description='This task belongs to user',
            user=self.user
        )
        
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        
        # Authenticate as the other user
        self.client.force_authenticate(user=other_user)
        
        # Try to delete the first user's task
        response = self.client.delete(f'/api/tasks/{task.id}/delete/')
        
        # Should return 404 because the task doesn't exist for this user
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Task not found or you do not have permission to delete it')
        
        # Verify the original task still exists
        self.assertTrue(Task.objects.filter(id=task.id).exists())
    
    def test_task_delete_nonexistent(self):
        """Test that deleting a non-existent task returns 404"""
        response = self.client.delete('/api/tasks/999/delete/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Task not found or you do not have permission to delete it')
    
    def test_task_delete_unauthenticated(self):
        """Test that unauthenticated users cannot delete tasks"""
        # Create a task
        from .models import Task
        task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            user=self.user
        )
        
        # Remove authentication
        self.client.force_authenticate(user=None)
        
        # Try to delete the task
        response = self.client.delete(f'/api/tasks/{task.id}/delete/')
        
        # Should return 401 for unauthenticated access
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify the task still exists
        self.assertTrue(Task.objects.filter(id=task.id).exists())
