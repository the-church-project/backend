from django.contrib import admin

from . import models as reading_models

# register your models here.

# admin.site.register(reading_models.BookCollection)
# admin.site.register(reading_models.Book)
# admin.site.register(reading_models.Chapter)
# admin.site.register(reading_models.Section)
# admin.site.register(reading_models.Verse)
admin.site.register(reading_models.Reading)
