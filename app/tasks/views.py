from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters


from user.utils import is_admin_user

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwner
# Create your views here.


class TaskViewSets(viewsets.ModelViewSet):
    """ A viewset for the Task Model. """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = "id"
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

    def get_queryset(self):
        """ Users can list only their events and admins can list all. """
        user = self.request.user
        
        if is_admin_user(user):
            return Task.objects.all()
        else:
            return Task.objects.filter(user=user)
    
    def get_object(self):
        # Custom logic to retrieve the object based on the request
        task_id = self.kwargs.get('id')

        # Customize the logic based on your requirements
        obj = get_object_or_404(Task, id=task_id)

        self.check_object_permissions(self.request, obj)

        return obj

    def perform_create(self, serializer):
        # Set the user of the task to the authenticated user during creation
        serializer.save(user=self.request.user)
