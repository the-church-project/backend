from django.contrib import admin

from .models import ErrorLog, Family, FamilyCard, User

# register your models here.

admin.site.register(User)
admin.site.register(Family)
admin.site.register(FamilyCard)
admin.site.register(ErrorLog)
