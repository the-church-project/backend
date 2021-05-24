from core import models as core_models
from core import serializers as core_serializers
from django.db import models
from django.urls import include, path
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
        fields = "__all__"


class ChapterSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = reading_models.Chapter
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = reading_models.Section
        fields = "__all__"


class VerseSerializer(serializers.ModelSerializer):
    section = SectionSerializer()
    chapter = ChapterSerializer()

    class Meta:
        model = reading_models.Verse
        fields = "__all__"


class ReadingSerializer(serializers.ModelSerializer):
    author = core_serializers.UserSerializer()

    class Meta:
        model = reading_models.Reading
        fields = "__all__"
