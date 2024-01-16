import pytest
from rest_framework import status
from django.urls import reverse

from .conftest import api_client_with_credentials
from ..models import Task


pytestmark = pytest.mark.django_db


class TestTasksEndPoints:
    list_create_task_url = reverse("task:task-list")

    def test_authenticated_user_can_create_task(self, api_client, authenticate_user):
        user = authenticate_user()
        token = user['token']

        data = {
            "title": "Test",
            "description": "Some info",
        }

        api_client_with_credentials(token, api_client)

        response = api_client.post(
            self.list_create_task_url, data=data)

        assert response.status_code == status.HTTP_201_CREATED

        assert response.json()['title'] == data['title']
        assert response.json()['description'] == data['description']

    def test_unauthenticated_user_cannot_create_task(self, api_client):

        data = {
            "title": "Test",
            "description": "Some info",
        }

        response = api_client.post(
            self.list_create_task_url, data=data, format='multipart')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_only_user_owned_tasks(self, task_factory, api_client, authenticate_user):
        """ List only tasks that belongs to the authenticated user. """
        user = authenticate_user()['user_instance']
        token = authenticate_user()['token']

        # Create 3 instances of task where 2 belongs to the current user.
        task_factory()
        task_factory.create_batch(2, user=user)

        api_client_with_credentials(token, api_client)

        response = api_client.get(self.list_create_task_url)

        results = response.json()['results']

        assert response.status_code == status.HTTP_200_OK

        assert len(results) == 2

    def test_unauthenticated_user_cannot_access_tasks_list(self, api_client):

        response = api_client.get(self.list_create_task_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_owner_can_delete_task(self, task_factory, api_client, authenticate_user):

        user = authenticate_user()
        task = task_factory(user=user['user_instance'])
        token = user['token']

        api_client_with_credentials(token, api_client)

        delete_task_url = reverse('task:task-detail', args=[task.id])

        # Make a DELETE request to delete the task
        response = api_client.delete(delete_task_url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Task.objects.count() == 0

    def test_non_owner_cannot_delete_task(self, task_factory, api_client, authenticate_user):

        task = task_factory()
        user = authenticate_user()
        token = user['token']

        api_client_with_credentials(token, api_client)

        delete_task_url = reverse('task:task-detail', args=[task.id])

        # Make a DELETE request to delete the task
        response = api_client.delete(delete_task_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_user_cannot_delete_tasks(self, task_factory, api_client):

        task = task_factory()

        delete_task_url = reverse('task:task-detail', args=[task.id])

        # Make a DELETE request to delete the task
        response = api_client.delete(delete_task_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_owner_can_update_task(self, task_factory, api_client, authenticate_user):

        user = authenticate_user()['user_instance']
        token = authenticate_user()['token']
        task = task_factory(title="Test 1", user=user)

        data = {
            "title": "Test updated"
        }

        update_task_url = reverse('task:task-detail', args=[task.id])

        api_client_with_credentials(token, api_client)
        response = api_client.patch(update_task_url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['title'] == data['title']

    def test_non_owner_cannot_update_task(self, task_factory, api_client, authenticate_user):

        token = authenticate_user()['token']
        task = task_factory(title="Test 1")

        data = {
            "title": "Test updated"
        }

        update_task_url = reverse('task:task-detail', args=[task.id])

        api_client_with_credentials(token, api_client)

        response = api_client.patch(update_task_url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_user_cannot_update_taskss(self, task_factory, api_client):
        task = task_factory(title="Test")
        data = {
            "title": "Test updated"
        }
        update_task_url = reverse('task:task-detail', args=[task.id])
        response = api_client.patch(update_task_url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_task_owner_can_retrieve_task(self, task_factory, api_client, authenticate_user):
        user = authenticate_user()['user_instance']
        token = authenticate_user()['token']
        task = task_factory(user=user)

        api_client_with_credentials(token, api_client)
        retrieve_task_url = reverse(
            'task:task-detail', args=[task.id])
        response = api_client.get(retrieve_task_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['title'] == task.title

    def test_non_task_owner_cannot_retrieve_task(self, task_factory, api_client, authenticate_user):
        token = authenticate_user()['token']
        task = task_factory()

        api_client_with_credentials(token, api_client)
        retrieve_task_url = reverse('task:task-detail', args=[task.id])
        response = api_client.get(retrieve_task_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_non_authenticated_user_cannot_retrieve_task(self, task_factory, api_client, authenticate_user):
        task = task_factory()

        retrieve_task_url = reverse('task:task-detail', args=[task.id])
        response = api_client.get(retrieve_task_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
