from datetime import timedelta
from typing import Any
import urllib.parse
import requests
import ast

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Book
from .forms import CreateForm, SearchForm, ProgressForm




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


class ReaderList(LoginRequiredMixin, FormView):
    model = Book
    template_name = 'reading_tracker/book_list.html'
    form_class = ProgressForm
    fields = ['current_page', 'current_time']
    success_url = reverse_lazy('reader')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(user=self.request.user)

        for book in context['books']:
            setattr(book, 'progress_form', ProgressForm(initial={
                'id': book.pk,
                'current_page': book.current_page,
                'current_time': book.current_time
            }))

        # search function
        search_input = self.request.GET.get('search-area', '')
        if search_input:
            context['books'] = context['books'].filter(title__icontains=search_input)

        return context
    
    def form_valid(self, form):
        book_id = self.request.POST.get('id')
        posted_page = self.request.POST.get('current_page')
        posted_time = self.request.POST.get('current_time')
        Book.objects.filter(user=self.request.user, pk=book_id).update(current_page=posted_page, current_time=posted_time)

        return super().form_valid(form)


class ReaderSearch(LoginRequiredMixin, FormView):
    template_name = 'reading_tracker/book_search.html'
    form_class = SearchForm

    def form_valid(self, form):
        # if posted form is search form, do search form stuff, else if form is result form, do result form stuff
        if 'search_query' in self.request.POST:
            search_query = form.cleaned_data['search_query']
            api_url = f'https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote_plus(search_query)}'
            response = requests.get(api_url)
            data = response.json()

            # if request is successful, return books using context vars
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
                    
                    book['volumeInfo']['coverUrl'] = f"https://books.google.com/books/content?id={book['id']}&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api"

                context = {
                    'form': SearchForm,
                    'book_request_bool': True, # tells front end whether or not search request was attempted
                    'book_count': book_count,
                    'books': books,
                }

                return render(self.request, self.template_name, context)
        
        # if results form, set session variable to form data (the user's chosen book) and redirect to ReaderCreate
        elif 'book_data' in self.request.POST:
            self.request.session['book_data'] = self.request.POST.get('book_data')

            return HttpResponseRedirect(reverse_lazy('book-create'))
        
        # return default search view page if form isn't recognized
        context = {
            'form': SearchForm,
            'book_request_bool': False,
        }

        return render(self.request, self.template_name, context)


class ReaderCreate(LoginRequiredMixin, CreateView):
    template_name = 'reading_tracker/book_create.html'
    model = Book
    form_class = CreateForm
    success_url = reverse_lazy('reader')

    def get_initial(self):
        # tries to load in session data as initial variables if it exists
        try:
            book_data_str = self.request.session['book_data']
            book_data = ast.literal_eval(book_data_str)

            cover_url = book_data['volumeInfo'].get('coverUrl', '')
            title = book_data['volumeInfo'].get('title', '')
            author = book_data['volumeInfo'].get('authors', '')
            publisher = book_data['volumeInfo'].get('publisher', '')
            description = book_data['volumeInfo'].get('description', '')
            gbooks_id = book_data['id']
            length_pages = book_data['volumeInfo'].get('pageCount', 0)

            self.request.session.pop('book_data')

            return {
                'cover_url': cover_url,
                'title': title,
                'author': author,
                'publisher': publisher,
                'description': description,
                'gbooks_id': gbooks_id,
                'length_pages': length_pages,
            }
        
        except:
            pass

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(ReaderCreate, self).form_valid(form)


class ReaderUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'reading_tracker/book_update.html'
    model = Book
    fields = ['title', 'author', 'publisher', 'description', 'book_type', 'length_pages', 'length_time', 'status', 'current_page', 'current_time']
    success_url = reverse_lazy('reader')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.get_object()

        return context


class ReaderDelete(LoginRequiredMixin, DeleteView):
    model = Book
    context_object_name = 'book'
    success_url = reverse_lazy('reader')