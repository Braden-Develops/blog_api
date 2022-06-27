from django.db import models

# Create your models here.


class Post(models.Model):
    creationtimestamp = models.DateTimeField(auto_now_add=True)
    modificationtimestamp = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    abstract = models.TextField(max_length=1000)
    body = models.TextField()

    class Meta:
        ordering = ['creationtimestamp']
