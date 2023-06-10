from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Books(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    total_pages = models.PositiveIntegerField(default=0)
    current_page = models.PositiveIntegerField(default=0)
    date_started = models.DateField(default=timezone.now, editable=True)
    date_finished = models.DateField(editable=True, blank=True, null=True)