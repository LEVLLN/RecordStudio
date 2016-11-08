from __future__ import unicode_literals

import re
import unicodedata

from django import forms
from django.contrib.auth import (
    get_user_model, password_validation,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _


class FirstNameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super(FirstNameField, self).to_python(value))


class LastNameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super(LastNameField, self).to_python(value))


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super(UsernameField, self).to_python(value))


class EmailField(forms.EmailField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super(EmailField, self).to_python(value))


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'email_error': _("The email is incorrect."),
        'email_error2': _("The email address is already used."),
        'first_name_error': _("The first name must not contain any digit numbers."),
        'last_name_error': _("The last name must not contain any digit numbers."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    first_name = forms.CharField(
        label='Enter your name',
        max_length=25,
        widget=forms.TextInput,
    )
    last_name = forms.CharField(
        label='Enter your last name',
        max_length=30,
    )
    email = forms.EmailField(
        label='Enter your email address',
        max_length=50,
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        field_classes = {'username': UsernameField,
                         "first_name": FirstNameField,
                         "last_name": LastNameField,
                         "email": EmailField}

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': ''})

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        result = re.search(r"[0-9]+", first_name)
        if result:
            raise forms.ValidationError(
                self.error_messages['first_name_error'],
                code='first_name_error', )
        else:
            return self.cleaned_data['first_name']

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        result = re.search(r"[0-9]+", last_name)
        if result:
            raise forms.ValidationError(
                self.error_messages['last_name_error'],
                code='last_name_error', )
        else:
            return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        active_user = get_user_model()._default_manager.filter(
            email__iexact=email, is_active=True)
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError(
                self.error_messages['email_error'],
                code='email_error', )
        if active_user:
            raise ValidationError(
                self.error_messages['email_error2'],
                code='email_error2', )
        else:
            return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2
