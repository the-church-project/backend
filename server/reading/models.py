# import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

# Create your models here.


class BookCollection(models.Model):
    title = models.CharField(_("Name of the collection"), max_length=128)
    description = models.CharField(_("description"), max_length=128)
    is_locked = models.BooleanField(default=False)


class Book(models.Model):
    title = models.CharField(_("Title of the book"), max_length=128)
    author = models.CharField(_("Name of the authors"),
                              max_length=128, blank=True, null=True)
    book_collection = models.ForeignKey(BookCollection, on_delete=models.CASCADE)

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


class Section(models.Model):
    title = models.CharField(_("Title of section"), max_length=256)


class Verse(models.Model):
    number = models.PositiveIntegerField(
        help_text="if the verse is in two chapters then the half of what is in the next chapter will have number 0")
    content = models.TextField()
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, blank=True, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)


class Reading(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    content = models.TextField()
    image = models.FilePathField(null=True,blank=True)
    date_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField()
    author = models.ForeignKey("core.User", on_delete=models.CASCADE)
