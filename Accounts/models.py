from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    last_login = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'Users'


class UserLastActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    last_login = models.DateTimeField(editable=False, null=True, blank=True)
    last_request = models.DateTimeField(editable=False)
    last_request_type = models.CharField(max_length=30, editable=False)
    last_request_IP = models.GenericIPAddressField(editable=False, null=True, blank=True)

    class Meta:
        db_table = 'Users_Last_Activities'
        verbose_name_plural = 'Users Last Activities'
