import secrets

from django.db import models

from django.contrib.auth.models import AbstractUser
from apps.core.models import BaseModel


class User(AbstractUser):
    pass


def _generate_gathering_code():
    return secrets.token_urlsafe(6)


class Gathering(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=32, unique=True, default=_generate_gathering_code)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_gatherings')
    members = models.ManyToManyField(User, related_name='user_gatherings', blank=True)

    def __str__(self):
        return self.name
