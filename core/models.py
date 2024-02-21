from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    OPS_USER = 'OPS'
    CLIENT_USER = 'CLIENT'
    USER_TYPE_CHOICES = [
        ('OPS_USER', 'OPS_USER'),
        ('CLIENT_USER', 'CLIENT_USER'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True, blank=True, null=True)

class File(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)