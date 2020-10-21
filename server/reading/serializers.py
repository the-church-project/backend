from django.urls import path, include
from reading import models as reading_models
from rest_framework import serializers, viewsets
from rest_framework.authtoken.models import Token


class BookCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = reading_models.BookCollection
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    book_collection = BookCollectionSerializer()
    class Meta:
        model = reading_models.Book
        fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    class Meta:
        model = reading_models.Chapter
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = reading_models.Section
        fields = '__all__'

class VerseSerializer(serializers.ModelSerializer):
    section = SectionSerializer()
    chapter = ChapterSerializer()
    class Meta:
        model = reading_models.Verse
        fields = '__all__'





class BookCollectionViewset(viewsets.ModelViewSet):
    queryset = reading_models.BookCollection.objects.all()
    serializer_class = BookCollectionSerializer

class BookViewset(viewsets.ModelViewSet):
    queryset = reading_models.Book.objects.all()
    serializer_class = BookSerializer

class ChapterViewset(viewsets.ModelViewSet):
    queryset = reading_models.Chapter.objects.all()
    serializer_class = ChapterSerializer

class SectionViewset(viewsets.ModelViewSet):
    queryset = reading_models.Section.objects.all()
    serializer_class = SectionSerializer

class VerseViewset(viewsets.ModelViewSet):
    queryset = reading_models.Verse.objects.all()
    serializer_class = VerseSerializer
