import pytest
from django.urls import reverse
from rest_framework import status

from .conftest import api_client_with_credentials

pytestmark = pytest.mark.django_db


class TestAuthEndpoints:

    login_url = reverse("auth:login")
    password_change_url = reverse('auth:password-change-list')

    def test_user_login(self, api_client, active_user, auth_user_password):
        data = {
            "email": active_user.email,
            "password": auth_user_password
        }
        response = api_client.post(self.login_url, data)
        assert response.status_code == status.HTTP_200_OK
        returned_json = response.json()
        assert 'refresh' in returned_json
        assert 'access' in returned_json

    def test_deny_login_to_inactive_user(self, api_client, inactive_user, auth_user_password):
        data = {
            "email": inactive_user.email,
            "password": auth_user_password
        }
        response = api_client.post(self.login_url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_deny_login_invalid_credentials(self, api_client, active_user):
        data = {
            "email": active_user.email,
            "password": "wrong@pass"
        }
        response = api_client.post(self.login_url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_change_password_using_valid_old_password(self, api_client, authenticate_user, auth_user_password):
        user = authenticate_user()
        token = user['token']
        user_instance = user['user_instance']
        data = {
            'old_password': auth_user_password,
            'new_password': 'newpass@@',
        }
        api_client_with_credentials(token, api_client)
        response = api_client.post(
            self.password_change_url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        user_instance.refresh_from_db()
        assert user_instance.check_password('newpass@@')

    def test_deny_change_password_using_invalid_old_password(self, api_client, authenticate_user):
        user = authenticate_user()
        token = user['token']
        data = {
            'old_password': 'invalidpass',
            'new_password': 'New87ge&nerated',
        }
        api_client_with_credentials(token, api_client)
        response = api_client.post(
            self.password_change_url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_deny_change_password_for_unathenticated_user(self, api_client):
        """Only Authenticated User can change password using old valid password"""
        data = {
            'old_password': 'invalidpass',
            'new_password': 'New87ge&nerated',
        }
        response = api_client.post(
            self.password_change_url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


