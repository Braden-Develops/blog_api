from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Post(models.Model):
    creationtimestamp = models.DateTimeField(auto_now_add=True)
    modificationtimestamp = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    abstract = models.TextField(max_length=1000)
    body = models.TextField()

    class Meta:
        ordering = ['creationtimestamp']


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
