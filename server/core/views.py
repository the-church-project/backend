from django.shortcuts import render
from django.contrib.auth.views import LoginView
from . import forms
from django.views.generic import TemplateView, CreateView
# Create your views here.

class UserCreateView(CreateView):
    form_class = forms.UserRegister
    template_name = 'auth/user_create.html'
    success_url = '/login/'

class LoginView(LoginView):
    template_name = 'auth/login.html'
    form_class = forms.UserLogin
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # context['referrer'] = self.request.GET.get('referrer',None)
        context['title'] = 'Login'
        return context

class HomeView(TemplateView):
    template_name = 'index.html'