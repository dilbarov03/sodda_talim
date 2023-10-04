from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.users.managers import UserManager
from django.utils import timezone

class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    phone = models.CharField(max_length=10, unique=True)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    subscribe_from = models.DateField(null=True, blank=True)
    subscribe_to = models.DateField(null=True, blank=True)
    objects = UserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    

    def has_active_subscription(self):
        if self.subscribe_from and self.subscribe_to:
            return self.subscribe_from <= timezone.now().date() <= self.subscribe_to
        return False
    