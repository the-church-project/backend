import phonenumber_field
from django.urls import include, path
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.fields import ReadOnlyField, SerializerMethodField

from . import models as core_models


class UserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    # token = serializers.SerializerMethodField()

    # def get_token(self, obj):
    #     try:
    #         token = Token.objects.get(user_id=obj.id)
    #         return token.key
    #     except Token.DoesNotExist:
    #         return "token failed create a new one"

    class Meta:
        model = core_models.User
        # fields = '__all__'
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'family']


class FamilySerializer(serializers.ModelSerializer):
    family_members = SerializerMethodField()
    hash_number = ReadOnlyField()

    def get_family_members(self, obj):
        q = core_models.User.objects.filter(
            family=obj.pk, family__isnull=False)
        return UserSerializer(q, many=True).data

    class Meta:
        model = core_models.Family
        fields = ['id','family_name', 'hash_number', 'family_members']


class FamilyCardSerializer(serializers.ModelSerializer):
    family = FamilySerializer()

    # def get_family(self, obj):
    #     objects = core_models.Family.objects.get(pk=obj.family.pk)
    #     fam_details = FamilySerializer(objects, many=True)

    class Meta:
        model = core_models.FamilyCard
        fields = ["card_number", "expiry_date", "family"]
