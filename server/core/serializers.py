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
    phone_number = PhoneNumberField(required=False)
    full_name = ReadOnlyField()

    class Meta:
        model = core_models.User
        fields = [
            'id',
            'full_name',
            'phone_number',
        ]
        extra_kwargs = {
            'id': {
                'required': True
            },
        }


class FamilySerializer(serializers.ModelSerializer):
    family_members = UserSerializerSmall(many=True, required=False)
    hash_number = ReadOnlyField()

    def get_family_members(self, obj):
        q = core_models.User.objects.filter(family=obj.pk,
                                            family__isnull=False)
        return UserSerializerSmall(q, many=True).data

    def create(self, obj):
        family_members = getattr(obj, 'family_members', [])
        family = self.Meta.model.objects.create(**obj)
        family.family_members.set([
            self.context['request'].user,
        ])
        return family

    def update(self, instance, validated_data):
        fam_members = getattr(validated_data, 'family_members', [])
        if instance.family_members.filter(id=self.context['request'].user.id):
            fam = super().update(instance, validated_data)
            if fam_members:
                fam.family_members.set([
                    *fam_members,
                ])
            return fam
        else:
            raise Exception("Cannot Edit Family if not a part of it")


    class Meta:
        model = core_models.Family
        fields = [
            'id',
            'family_name',
            'hash_number',
            'family_members',
        ]


class FamilyCardSerializer(serializers.ModelSerializer):
    family = FamilySerializer()

    # def get_family(self, obj):
    #     objects = core_models.Family.objects.get(pk=obj.family.pk)
    #     fam_details = FamilySerializer(objects, many=True)

    class Meta:
        model = core_models.FamilyCard
        fields = ["card_number", "expiry_date", "family"]
