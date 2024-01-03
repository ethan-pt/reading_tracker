import datetime
import requests

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Book, ReadingStatus, ReadingProgress
from .forms import CreateForm, SearchForm

import urllib.parse
import requests



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
    form_class = SearchForm

    def form_valid(self, form):
        # if posted form is search form, do search form stuff, else if form is result form, do result form stuff
        if form.fields['search_query']:
            search_query = form.cleaned_data['search_query']
            api_url = f'https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote_plus(search_query)}'
            response = requests.get(api_url)
            data = response.json()

            # if request is successful, return request data, else return false success bool so front end knows to display error message
            if response.status_code == 200 and data.get('totalItems'):
                book_count = data.get('totalItems')
                books = data.get('items')

                # this for loop iterates through book objects returned and adds cover photo and 
                # replaces authors list with a joined string for each book in returned book data
                for book in books:
                    if book['volumeInfo'].get('authors'):
                        book['volumeInfo']['authors'] = ', '.join(book['volumeInfo']['authors'])
                    else:
                        book['volumeInfo']['authors'] = 'Author not found'
                    
                    book['cover'] = f"https://books.google.com/books/content?id={book['id']}&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api"

                context = {
                    'form': SearchForm,
                    'success_bool': True, # tells front end whether or not search request was successful
                    'book_count': book_count,
                    'books': books,
                }
            
            else:
                context = {
                    'form': SearchForm,
                    'success_bool': False
                }

            return render(self.request, self.template_name, context)
        
        # if results form, set session variable to form data (the user's chosen book) and redirect to ReaderCreate
        elif form.fields['book-id']:
            self.request.session['result_data'] = form.cleaned_data['book-id']

            redirect('book-create')



class ReaderCreate(LoginRequiredMixin, CreateView):
    model = Book
    form_class = CreateForm
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