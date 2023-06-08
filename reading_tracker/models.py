from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator



class Books(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    total_pages = models.IntegerField(validators=[MinValueValidator(0)])
    current_page = models.IntegerField(default=0, validators=[MaxValueValidator(total_pages), MinValueValidator(0)])
    date = models.DateField(auto_now_add=True)