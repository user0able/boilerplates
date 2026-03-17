import pytest

from apps.users.models import User
from apps.users.serializers import UserSerializer


@pytest.mark.django_db
class TestUserSerializer:
    def test_serializer_fields(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        serializer = UserSerializer(user)
        assert set(serializer.data.keys()) == {"id", "username", "email", "first_name", "last_name"}

    def test_id_is_read_only(self):
        serializer = UserSerializer()
        assert serializer.fields["id"].read_only
