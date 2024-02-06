from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta



class Book(models.Model):
    BOOK_TYPE_CHOICES = [
        ('paper-book', 'paper book'),
        ('e-book', 'e-book'),
        ('audio-book', 'audio book')
    ]
    STATUS_CHOICES = [
        ('reading', 'Reading'),
        ('finished', 'Finished!'),
        ('gave-up', 'Gave Up'),
        ('want-to-read', 'Want to Read'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_url = models.URLField(blank=True, null=True)
    gbooks_id = models.CharField(max_length=12, unique=True, blank=True, null=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    book_type = models.CharField(choices=BOOK_TYPE_CHOICES)
    length_pages = models.PositiveIntegerField(blank=True, null=True)
    length_time = models.DurationField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    current_page = models.PositiveIntegerField(blank=True, null=True, default=0)
    current_time = models.DurationField(blank=True, null=True, default=timedelta)
    last_updated = models.DateTimeField(auto_now=True)