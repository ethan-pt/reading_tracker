from django.db import models
from django.contrib.auth.models import User



class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    length = models.PositiveIntegerField()