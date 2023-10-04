import datetime

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
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
            return reverse_lazy('reader')
        
        return super(ReaderRegister, self).get(*args, **kwargs)
    

class ReaderList(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # search function
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['book'] = context['book'].filter(title__icontains=search_input)

        context['search-input'] = search_input

        return context
    

class ReaderCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'description', 'total_pages', 'date_started']
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