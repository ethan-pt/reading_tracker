from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError



class Books(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    total_pages = models.PositiveIntegerField(default=0)
    current_page = models.PositiveIntegerField(default=0)
    date_started = models.DateField(default=timezone.now, editable=True)
    date_finished = models.DateField(editable=True, blank=True, null=True)

    class Meta:
        ordering = ['-date_started']

    def clean(self):
        if self.current_page:
            if self.current_page > self.total_pages:
                raise ValidationError('Current page cannot exceed total pages.')
        
            if self.current_page != self.total_pages and self.complete:
                raise ValidationError('Make sure current page reflects book status.')
        
        if self.date_finished and self.date_started > self.date_finished:
            raise ValidationError('Date started cannot exceed date finished.')