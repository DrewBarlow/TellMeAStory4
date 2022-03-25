from django.db import models

# Create your models here.
class User(models.Model):
    username: str = models.CharField(max_length=200)
    password: str = models.CharField(max_length=512)
    display_name: str = models.CharField(max_length=200)
