from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
import uuid


class UsernameField(models.CharField):
    def get_prep_value(self, value):
        return str(value).lower()


class UserEmailField(models.EmailField):
    def get_prep_value(self, value):
        return str(value).lower()


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = UserEmailField(unique=True)
    username = UsernameField(max_length=150, unique=True,
                             help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                             error_messages={'unique': 'A user with that username already exists.'},
                             validators=[UnicodeUsernameValidator()])
    is_staff = models.BooleanField(default=False,
                                   help_text='Designates whether the user is administrator of this site.',)
    last_request = models.DateTimeField(null=True, blank=True, editable=False)
    last_IP = models.GenericIPAddressField(null=True, blank=True, editable=False)
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return str(self.username).capitalize()

    class Meta:
        db_table = 'Users'
