from django.contrib import admin

from .models import Family, FamilyCard, User

# Register your models here.


class FamilyAdmin(admin.ModelAdmin):
    readonly_fields = [
        'members',
    ]


admin.site.register(User)
admin.site.register(Family, FamilyAdmin)
admin.site.register(FamilyCard)
