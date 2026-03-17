import pytest
from rest_framework.test import APIClient

from apps.users.models import User


@pytest.mark.django_db
class TestUserViewSet:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_list_users(self):
        response = self.client.get("/api/v1/users/")
        assert response.status_code == 200

    def test_retrieve_user(self):
        response = self.client.get(f"/api/v1/users/{self.user.pk}/")
        assert response.status_code == 200
        assert response.data["username"] == "testuser"
        assert response.data["email"] == "test@example.com"

    def test_unauthenticated_access_denied(self):
        client = APIClient()
        response = client.get("/api/v1/users/")
        assert response.status_code in (401, 403)
