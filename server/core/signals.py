from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models as core_models
# from django.conf import settings
# from rest_framework.authtoken.models import Token

from . import models as core_models


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


@receiver(post_save, sender=core_models.Family)
def create_familyCard(sender, instance=None, created=False, **kwargs):
    if created:
        core_models.FamilyCard.objects.create(family=instance)
