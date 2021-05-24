"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from rest_framework.authtoken import views
from core import serializers as core_serializers
from core import views as core_views
from django.contrib import admin
from django.urls import include, path
from reading import serializers as reading_serializers
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user', core_serializers.UserViewset)
router.register(r'family', core_serializers.FamilyViewset)
router.register(r'familycard', core_serializers.FamilyCardViewset)

router_reading = routers.DefaultRouter()
router_reading.register(
    r'collection', reading_serializers.BookCollectionViewset)
router_reading.register(r'book', reading_serializers.BookViewset)
router_reading.register(r'chapter', reading_serializers.ChapterViewset)
router_reading.register(r'section', reading_serializers.SectionViewset)
router_reading.register(r'verse', reading_serializers.VerseViewset)

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    # path('login/', views.obtain_auth_token),
    path('api/core/', include(router.urls)),
    path('api/reading/', include(router_reading.urls)),
    # path('api/', include(router.urls)),
    path('api-token-auth/', core_views.CustomObtainAuthToken.as_view(), name='api-tokn-auth')
]
