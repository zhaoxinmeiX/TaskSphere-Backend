from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from .models import Task
from .serializers import TaskSerializer


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save(user=request.user)
        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_201_CREATED
        )


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                TaskSerializer(task).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
            task.delete()
            return Response(
                {'message': 'Task deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Task.DoesNotExist:
            return Response(
                {'error': 'Task not found or you do not have permission to delete it'},
                status=status.HTTP_404_NOT_FOUND
            )
