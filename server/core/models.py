import random

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token

# Create your models here.


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        # email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), null=True, blank=True)
    phone_number = PhoneNumberField(_("phone number"), unique=True)
    dob = models.DateField(null=True, blank=True)
    family = models.ForeignKey(
        "core.Family", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_poc = models.BooleanField(_("point of contact"), default=False)
    objects = UserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name"]

    def clean(self):
        """
        Clean up blank fields to null
        """
        if self.email == "":
            self.email = None

    def __str__(self):
        return f"{self.phone_number}"


class FamilyCard(models.Model):
    family = models.OneToOneField("core.Family", on_delete=models.CASCADE)
    card_number = models.IntegerField(_("card number"),null=True, blank=True, unique=True)
    issue_date = models.DateField(_("date of issue"),null=True, blank=True)
    expiry_date = models.DateField(_("date of expiry"),null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    def clean(self):
        """
        Clean up blank fields to null
        """
        if self.card_number == "":
            self.card_number = None

    def __str__(self):
        if self.card_number and self.is_verified:
            status = "OK"
        elif self.card_number:
            status = "VP"
        else:
            status = "NV"
        return f"{self.family.family_name}-{status}"


class Family(models.Model):
    # username_validator = UnicodeUsernameValidator()

    # username = models.CharField(
    #     _("username"),
    #     max_length=150,
    #     help_text=_(
    #         "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    #     ),
    #     validators=[username_validator],
    #     error_messages={
    #         "unique": _("A user with that username already exists."),
    #     },
    # )
    family_name = models.CharField(max_length=256)
    hash_number = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(99999),
        ],
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def members(self):
        q=User.objects.filter(family=self.pk).exclude(family__isnull=True).values_list('first_name')
        return self.query_to_string(q)

    @staticmethod
    def query_to_string(query, remove_items_list:str=''):
        string = ' '.join(map(str, query))
        return string.replace('(','').replace(')','').replace(',','\n').replace("'",'')


    def random_hash_generator(self):
        num = random.randint(0, 99999)
        try:
            self.objects.get(hash_number=num, family_name=self.family_name)
            self.random_hash_generator()
        except:
            return num

    def save(self, *args, **kwargs):
        if not self.hash_number:
            self.hash_number = self.random_hash_generator()
        super().save()

    def __str__(self):
        return f"{self.family_name} #{self.hash_number}"

    class Meta:
        unique_together = (
            "family_name",
            "hash_number",
        )
        verbose_name_plural = "Families"


class ErrorLog(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=256)
    description = models.TextField()

    def __str__(self):
        return f"{self.time}"
