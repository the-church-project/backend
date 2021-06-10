from django.contrib.auth import authenticate
from django.urls import include, path
from rest_framework import permissions, viewsets
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

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

    # def list(self, request):
    #     obj = self.get_object()
    #     serializer = self.serializer_class(obj)
    #     return Response(None)


class CreateUserViewset(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        usr_data = request.data
        password = usr_data.get('password')
        first_name = usr_data.get('first_name')
        last_name = usr_data.get('last_name')
        user = None
        try:
            user = core_models.User.objects.get(
                phone_number=usr_data['username'])
            return Response({
                'status': 'Error',
                'message': "User Already exists with this phone number try logging in or sign up with a new number"
            })
        except core_models.User.DoesNotExist:
            user = core_models.User.objects.create(
                first_name=first_name,
                last_name=last_name,
                phone_number=usr_data['username'],
            )
            user.set_password(password)
            user.save()
            return Response({
                'status': 'Success',
                'user_id': user.id
            })
        except Exception as e:
            return Response({'status': 'Error'})
        # finally:
            # login(request, user=user,
            #       backend='django.contrib.auth.backends.ModelBackend')


class CustomObtainAuthToken(views.ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        t = UserSerializer(user)
        return Response({'token': token.key, 'user': {**t.data}})
