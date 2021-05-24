import re

from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render
# from . import forms
from django.views.generic import CreateView, TemplateView
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import UserSerializer

# Create your views here.

# class UserCreateView(CreateView):
#     form_class = forms.UserRegister
#     template_name = 'auth/user_create.html'
#     success_url = '/login/'

# class LoginView(LoginView):
#     template_name = 'auth/login.html'
#     form_class = forms.UserLogin
#     def get_context_data(self,**kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['referrer'] = self.request.GET.get('referrer',None)
#         context['title'] = 'Login'
#         return context

# class HomeView(TemplateView):
#     template_name = 'index.html'


class CustomObtainAuthToken(views.ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        t = UserSerializer(user)
        return Response({'token': token.key, **t.data})
