from django.urls import include, path
from reading import models as reading_models
from rest_framework import viewsets
from rest_framework.authtoken.models import Token

from .serializers import *


class BlogViewset(viewsets.ModelViewSet):
    queryset = reading_models.Blog.objects.order_by('-date_time', '-end_time')
    serializer_class = BlogSerializer

# class BookCollectionViewset(viewsets.ModelViewSet):
#     queryset = reading_models.BookCollection.objects.all()
#     serializer_class = BookCollectionSerializer


# class BookViewset(viewsets.ModelViewSet):
#     queryset = reading_models.Book.objects.all()
#     serializer_class = BookSerializer


# class ChapterViewset(viewsets.ModelViewSet):
#     queryset = reading_models.Chapter.objects.all()
#     serializer_class = ChapterSerializer


# class SectionViewset(viewsets.ModelViewSet):
#     queryset = reading_models.Section.objects.all()
#     serializer_class = SectionSerializer


# class VerseViewset(viewsets.ModelViewSet):
#     queryset = reading_models.Verse.objects.all()
#     serializer_class = VerseSerializer
