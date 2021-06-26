import datetime

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Blog(models.Model):
    DEFAULT_HOURS = 24

    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    content = models.TextField()
    date_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(
        "core.User", on_delete=models.SET_NULL, null=True)
    # image = models.ImageField(null=True,blank=True)

    @classmethod
    def with_hours(cls, title, content, author, description='', hours=''):
        end_time = now() + datetime.timedelta(hours=hours) if hours else ''
        return cls(title=title, end_time=end_time, description=description, content=content, author=author)

    def save(self):
        if not self.end_time:
            self.end_time = now() + datetime.timedelta(hours=self.DEFAULT_HOURS)
        super().save()

    def __str__(self):
        return f"{self.title} - {self.date_time}"

# class BookCollection(models.Model):
#     title = models.CharField(_("Name of the collection"), max_length=128)
#     description = models.CharField(_("description"), max_length=128)
#     is_locked = models.BooleanField(default=False)
#     # multiple = models.ManyToManyField('reading.BookCollection')


# class Book(models.Model):
#     title = models.CharField(_("Title of the book"), max_length=128)
#     author = models.CharField(
#         _("Name of the authors"), max_length=128, blank=True, null=True
#     )
#     book_collection = models.ForeignKey(
#         BookCollection, on_delete=models.CASCADE)


# class Chapter(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)


# class Section(models.Model):
#     title = models.CharField(_("Title of section"), max_length=256)


# class Verse(models.Model):
#     number = models.PositiveIntegerField(
#         help_text="if the verse is in two chapters then the half of what is in the next chapter will have number 0"
#     )
#     content = models.TextField()
#     section = models.ForeignKey(
#         Section, on_delete=models.CASCADE, blank=True, null=True
#     )
#     chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
