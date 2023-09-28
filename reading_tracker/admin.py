from django.contrib import admin
from .models import Book, ReadingStatus, ReadingProgress



admin.site.register(Book)
admin.site.register(ReadingStatus)
admin.site.register(ReadingProgress)