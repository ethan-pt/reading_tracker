from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator



class Book(models.Model):
    BOOK_TYPE_CHOICES = [
        ('paper book', 'paper book'),
        ('e-book', 'e-book'),
        ('audio book', 'audio book')
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    book_type = models.CharField(choices=BOOK_TYPE_CHOICES)
    length_pages = models.PositiveIntegerField(blank=True)
    length_time = models.DurationField(blank=True)

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
    PROGRESS_CHOICES = [
        ('Page', 'Page')
        ('Percentage', 'Percentage'),
        ('Time', 'Time')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tracking_type = models.CharField(max_length=20, choices=PROGRESS_CHOICES)
    current_percent = models.PositiveIntegerField(validators=[MaxValueValidator(100)], blank=True)
    current_page = models.PositiveIntegerField(blank=True)
    current_time = models.DurationField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)