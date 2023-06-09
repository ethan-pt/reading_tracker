import datetime

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Books



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
    model = Books
    context_object_name = 'books'

    # filter function, returns list of books completed in current year
    def check_year(book):
        if book.complete == True and book.date.year == datetime.date.today().year:
            return True
        
        return False


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = context['books'].filter(user=self.request.user)
        context['finished'] = context['books'].filter(self.check_year)
        context['finished_count'] = context['finished'].count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['books'] = context['books'].filter(title__icontains=search_input)

        context['search-input'] = search_input

        return context