from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Modelo de usuario personalizado."""

    class Meta:
        db_table = "users"
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def __str__(self):
        return self.email or self.username
