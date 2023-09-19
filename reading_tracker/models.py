from django.db import models
from django.contrib.auth.models import User



class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    length = models.PositiveIntegerField()

class ReadingStatus(models.Model):
    STATUS_CHOICES = [
        ('Reading', 'Reading'),
        ('Finished!', 'Finished!'),
        ('Gave Up', 'Gave Up'),
        ('Want to Read', 'Want to Read'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

class ReadingProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    current_page = models.PositiveIntegerField(help_text="Page number for physical/digital books, percentage for audiobooks")
    last_updated = models.DateTimeField(auto_now=True)