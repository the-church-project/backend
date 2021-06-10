from django.contrib import admin

from .models import ErrorLog, Family, FamilyCard, User

# register your models here.


class FamilyAdmin(admin.ModelAdmin):
    readonly_fields = [
        'members',
    ]


admin.site.register(User)
admin.site.register(Family, FamilyAdmin)
admin.site.register(FamilyCard)
# admin.site.register(ErrorLog)
