from django.contrib.auth import authenticate
from django.urls import include, path
from rest_framework import viewsets
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from . import models as core_models
from .serializers import *


class FamilyViewset(viewsets.ModelViewSet):
    queryset = core_models.Family.objects.all()
    serializer_class = FamilySerializer


class FamilyCardViewset(viewsets.ModelViewSet):
    queryset = core_models.FamilyCard.objects.all()
    serializer_class = FamilyCardSerializer


class UserViewset(viewsets.ModelViewSet):
    queryset = core_models.User.objects.all()
    serializer_class = UserSerializer


class CustomObtainAuthToken(views.ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        t = UserSerializer(user)
        return Response({'token': token.key, 'user':{**t.data}})
