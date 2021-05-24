import re

from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView

from . import forms


# Create your views here.
# templates not available do not render theses views
class UserCreateView(CreateView):
    form_class = forms.UserRegister
    template_name = 'auth/user_create.html'
    success_url = '/login/'

class NewLoginView(LoginView):
    template_name = 'auth/login.html'
    form_class = forms.UserLogin
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # context['referrer'] = self.request.GET.get('referrer',None)
        context['title'] = 'Login'
        return context

class HomeView(TemplateView):
    template_name = 'index.html'
