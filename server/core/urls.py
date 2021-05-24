from django.contrib.auth.views import LogoutView
from django.urls import include, path

from . import views

app_name = 'core'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    # path('usercreate/', views.UserCreateView.as_view(),name='usercreate'),
    # path('', views.HomeView.as_view(), name='home'),
]
