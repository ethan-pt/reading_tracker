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
    
