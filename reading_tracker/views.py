import datetime
import requests

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Book, ReadingStatus, ReadingProgress



class ReaderLogin(LoginView):
    template_name = 'reading_tracker/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('reader')
    

class ReaderRegister(FormView):
    template_name = 'reading_tracker/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('reader')

    def form_valid(self, form):
        user = form.save()

        if user is not None:
            login(self.request, user)

        return super(ReaderRegister, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('reader')
        
        return super(ReaderRegister, self).get(*args, **kwargs)


class ReaderList(LoginRequiredMixin, ListView):
    model = ReadingStatus
    context_object_name = 'reading_statuses'

    def get_queryset(self):
        return ReadingStatus.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = [status.book for status in context['reading_statuses']]
        return context


class ReaderSearch(LoginRequiredMixin, FormView):
    template_name = 'reading_tracker/book_search.html'


class ReaderCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'publisher', 'gbooks_id', 'length_pages', 'length_time']
    success_url = reverse_lazy('reader')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(ReaderCreate, self).form_valid(form)


class ReaderUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'description', 'complete', 'current_page', 'total_pages', 'date_started', 'date_finished']
    success_url = reverse_lazy('reader')


class ReaderDelete(LoginRequiredMixin, DeleteView):
    model = Book
    context_object_name = 'book'
    success_url = reverse_lazy('reader')