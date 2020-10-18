import random
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator
# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_poc = models.BooleanField(_('point of contact'), default=False)


class FamilCard(models.Model):
    family = models.ForeignKey('core.Family', on_delete=models.CASCADE)
    card_number = models.IntegerField(_('card number'))
    issue_date = models.DateField(_('date of issue'))
    expiry_date = models.DateField(_('date of expiry'))

    def __str__(self):
        return f'{self.family.username}'


class Family(models.Model):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    hash_number = models.PositiveIntegerField(validators=[MaxValueValidator(100),])
    members = models.ManyToManyField('core.User')

    def random_hash_generator(self):
        num = random.randint(0,9999)
        try:
            self.objects.get(hash_number=num,username=self.username)
            self.random_hash_generator()
        except DoesNotExist:
            return num
    
    def save(self):
        if not self.hash_number:
            try:
                self.hash_number = self.random_hash_generator()
        super(Family,self).save()

    def __str__(self):
        return f'{self.family.username} #{self.hash_number}'


    class Meta:
        unique_together = ('username', 'hash_number',)