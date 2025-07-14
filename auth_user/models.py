from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    researcher = models.BooleanField(default=False)
    secretariat = models.BooleanField(default=False)
    stakeholder = models.BooleanField(default=False)
