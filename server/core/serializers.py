import phonenumber_field
from django.urls import include, path
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.fields import ReadOnlyField, SerializerMethodField

from . import models as core_models


class UserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    # def __init__(self, *args, **kwargs):
    #     remove_fields = kwargs.pop('remove_fields', None)
    #     if remove_fields: 
    #         for field_name in remove_fields:
    #             try:
    #                 self.Meta.fields.remove(field_name)
    #             except:
    #                 pass
    #     super().__init__(*args, **kwargs)

    class Meta:
        model = core_models.User
        # fields = '__all__'
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'family',
            'password',
            'dob',
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'family': {
                'read_only': True
            },
            'first_name': {
                'required': True
            }
        }


class UserSerializerSmall(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = core_models.User
        fields = [
            'id',
            'full_name',
            'phone_number',
        ]


class FamilySerializer(serializers.ModelSerializer):
    family_members = SerializerMethodField()
    hash_number = ReadOnlyField()

    def get_family_members(self, obj):
        q = core_models.User.objects.filter(family=obj.pk,
                                            family__isnull=False)
        return UserSerializerSmall(q, many=True).data

    class Meta:
        model = core_models.Family
        fields = ['id', 'family_name', 'hash_number', 'family_members']


class FamilyCardSerializer(serializers.ModelSerializer):
    family = FamilySerializer()

    # def get_family(self, obj):
    #     objects = core_models.Family.objects.get(pk=obj.family.pk)
    #     fam_details = FamilySerializer(objects, many=True)

    class Meta:
        model = core_models.FamilyCard
        fields = ["card_number", "expiry_date", "family"]
