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
from core import views as core_views
from core import viewsets as core_viewsets
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from reading import viewsets as reading_viewsets
from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()
router.register(r'user', core_viewsets.UserViewset)
router.register(r'family', core_viewsets.FamilyViewset)
router.register(r'familycard', core_viewsets.FamilyCardViewset)

router_reading = routers.DefaultRouter()
router_reading.register(r'blog', reading_viewsets.ReadingViewset)
# router_reading.register(
#     r'collection', reading_viewsets.BookCollectionViewset)
# router_reading.register(r'book', reading_viewsets.BookViewset)
# router_reading.register(r'chapter', reading_viewsets.ChapterViewset)
# router_reading.register(r'section', reading_viewsets.SectionViewset)
# router_reading.register(r'verse', reading_viewsets.VerseViewset)

development_urls = []

if settings.DEBUG:
    development_urls = [
        path("swagger<format>", viewsets.schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/',
             viewsets.schema_view.with_ui('swagger', cache_timeout=0),
             name='schema-swagger-ui'),
        path('redoc/',
             viewsets.schema_view.with_ui('redoc', cache_timeout=0),
             name='schema-redoc'),
    ]

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('api/create-user/', core_viewsets.CreateUserViewset.as_view()),
    path('api/core/', include(router.urls)),
    path('api/reading/', include(router_reading.urls)),
    path('api/api-token-auth/',
         core_viewsets.CustomObtainAuthToken.as_view(),
         name='api-token-auth')
] + development_urls
