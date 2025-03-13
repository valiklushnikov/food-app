from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ParseError


class CustomUserManager(BaseUserManager):
    use_in_mirgations = True

    def _create(self, email=None, password=None, **extra_fields):
        if not email:
            raise ParseError("Email is required")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", True)

        return self._create(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        return self._create(email, password, **extra_fields)
