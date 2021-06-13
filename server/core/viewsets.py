from django.contrib.auth import authenticate, login
from django.urls import include, path
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models as core_models
from .serializers import *

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsCreationOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            if view.action == 'create':
                return True
            else:
                return False
        else:
            return True


class FamilyViewset(viewsets.ModelViewSet):
    queryset = core_models.Family.objects.all()
    serializer_class = FamilySerializer


class FamilyCardViewset(viewsets.ModelViewSet):
    queryset = core_models.FamilyCard.objects.all()
    serializer_class = FamilyCardSerializer


class UserViewset(viewsets.ModelViewSet):
    permission_classes = [
        IsCreationOrIsAuthenticated,
    ]
    queryset = core_models.User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = core_models.User.objects.get(
                phone_number=serializer.validated_data['phone_number'])
            return Response(
                {
                    'message':
                    'User Already exists with this phone number try logging in or sign up with a new number'
                },
                status=status.HTTP_400_BAD_REQUEST)
        except core_models.User.DoesNotExist:
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    **serializer.data
                }
            },
                            status=status.HTTP_201_CREATED)

    # def list(self, request):
    #     obj = self.get_object()
    #     serializer = self.serializer_class(obj)
    #     return Response(None)


# class CreateUserViewset(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         usr_data = request.data
#         user = None
#         serializer = UserSerializer(data=usr_data)
#         serializer.is_valid(raise_exception=True)
#         try:
#             user = core_models.User.objects.get(
#                 phone_number=serializer.validated_data['phone_number'])
#             return Response(
#                 {
#                     'message':
#                     "User Already exists with this phone number try logging in or sign up with a new number"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST)
#         except core_models.User.DoesNotExist:
#             user = serializer.save()
#             serial = UserSerializer(user)
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({
#                 'token': token.key,
#                 'user': {
#                     **serial.data
#                 }
#             },
#                             status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({'message': e})
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
        return Response({
            'token': token.key,
            'user': {
                **t.data
            }
        },
                        status=status.HTTP_200_OK)
