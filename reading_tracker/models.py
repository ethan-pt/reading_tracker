from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from pkg_resources import require



class Book(models.Model):
    BOOK_TYPE_CHOICES = [
        ('paper-book', 'paper book'),
        ('e-book', 'e-book'),
        ('audio-book', 'audio book')
    ]

    cover_url = models.URLField(blank=True, null=True)
    gbooks_id = models.CharField(max_length=12, unique=True, blank=True, null=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    book_type = models.CharField(choices=BOOK_TYPE_CHOICES)
    length_pages = models.PositiveIntegerField(blank=True, null=True)
    length_time = models.DurationField(blank=True, null=True)

class ReadingStatus(models.Model):
    STATUS_CHOICES = [
        ('reading', 'Reading'),
        ('finished', 'Finished!'),
        ('gave-up', 'Gave Up'),
        ('want-to-read', 'Want to Read'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

class ReadingProgress(models.Model):
    PROGRESS_CHOICES = [
        ('page', 'Page'),
        ('percentage', 'Percentage'),
        ('time', 'Time')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tracking_type = models.CharField(max_length=20, choices=PROGRESS_CHOICES)
    current_percent = models.PositiveIntegerField(validators=[MaxValueValidator(100)], blank=True, null=True)
    current_page = models.PositiveIntegerField(blank=True, null=True)
    current_time = models.DurationField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)