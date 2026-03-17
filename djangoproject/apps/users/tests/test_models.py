import pytest

from apps.users.models import User


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.check_password("testpass123")

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
        )
        assert admin.is_superuser
        assert admin.is_staff

    def test_str_returns_email(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        assert str(user) == "test@example.com"

    def test_str_returns_username_when_no_email(self):
        user = User.objects.create_user(
            username="testuser",
            email="",
            password="testpass123",
        )
        assert str(user) == "testuser"
