# coding=utf-8
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class AuthorizationForm(forms.Form):
    password = forms.CharField(label=_('Password'))

    def check_password(self, valid_password):
        if self.cleaned_data['password'] == valid_password:
            return True

        self.add_error('password', ValidationError(_('Invalid password')))
        return False
