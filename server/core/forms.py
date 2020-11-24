from django import forms
import core.models as core_models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.text import gettext_lazy as _
from phonenumber_field.validators import validate_international_phonenumber as validate_phone
#create the custom forms for the core model

class UserLogin(forms.ModelForm):
    email_phone = forms.CharField(max_length=256)
    class Meta:
        model = core_models.User
        fields = ['email_phone', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        try:
            validate_email(cleaned_data.get('email_phone'))
            cleaned_data['email'] = cleaned_data.get('email_phone')
            return cleaned_data
        except ValidationError:
            try:
                validate_phone(cleaned_data.get('email_phone'))
                cleaned_data['phone_number'] = cleaned_data.get('email_phone')
                return cleaned_data
            except ValidationError:
                raise ValidationError(_('The given data is not a valid email or phone number'))

class UserRegister(forms.ModelForm):
    email = forms.EmailField(renderer=False)
    confirm_password = forms.CharField(min_length=8,max_length=128)
    password = forms.CharField(min_length=8,max_length=128)

    class Meta:
        model = core_models.User
        fields = [ 'phone_number','email','first_name', 'last_name','password','confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('password') == cleaned_data.get('confirm_password'):
            raise ValidationError('passwords do not match please re-try')
        if self.Meta.model.objects.filter(email=cleaned_data.filter('email')).exists():
            raise ValidationError('email already exists try loging in or retry with a new email')
        if self.Meta.model.objects.filter(phone_number=cleaned_data.filter('phone_number')).exists():
            raise ValidationError('phone number already exists try loging in or retry with a new phone number')

class FamilyRegister(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FamilyRegister, self).__init__(*args, **kwargs)

    class Meta:
        model = core_models.Family
        fields = ['username', 'family_name']

class FamilyAdd(forms.ModelForm):
    class Meta:
        model = core_models.Family
        fields = ['family_name', 'username', 'hash_number']