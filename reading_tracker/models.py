from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator



class Books(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    total_pages = models.PositiveIntegerField(default=0)
    current_page = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(total_pages)])
    date = models.DateField(auto_now_add=True)