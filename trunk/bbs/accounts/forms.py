#!/usr/bin/env python
#coding=utf-8


from django import forms
from django.utils.translation import ugettext as _T
from django.contrib.auth.models import User, check_password

import accounts.tools;
import accounts.config;

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, label=_T('User Name'))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput, label=_T('Password'))
    saveLogin = forms.BooleanField(required=False, label=_T('Remember my login'))
    next = forms.CharField(required=False, widget=forms.HiddenInput, label=_T('Next Page'))
    validation = forms.CharField(max_length=5, label=_T('Validation Code'))

    def clean_username(self):
        user = accounts.tools.finduser(self.cleaned_data['username'])
        if user:
            self.cleaned_data['user'] = user
            return self.cleaned_data['username']
        else:
            raise forms.ValidationError(_T("The user does not exist!"))

    def clean_validation(self):
        if self.code == "":
            raise forms.ValidationError(_T("The validation code has expired!"))
        elif self.cleaned_data['validation'] != self.code:
            raise forms.ValidationError(_T("Invalid validation code!"))
        else:
            return self.cleaned_data['validation']

    def clean(self):
        if not self.hasCookie:
            raise forms.ValidationError(_T("Cookie is required!"))
        elif len(self.errors) == 0:
            cleaned_data = forms.Form.clean(self)
            if check_password(cleaned_data['password'], self.cleaned_data['user'].user.password):
                return cleaned_data
            else:
                self.errors['password'] = forms.ValidationError(_T("Invalid Password!"))
                raise self.errors['password']
        else:
            return None

    

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=200, label=_T('User Name'))
    email = forms.EmailField(label=_T('e-Mail'))
    password1 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput, label=_T('Password 1'))
    password2 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput, label=_T('Password 2'))
    validation = forms.CharField(max_length=5, label=_T('Validation Code'))
    next = forms.CharField(required=False, widget=forms.HiddenInput, label=_T('Next Page'))

    def clean_username(self):
        n = User.objects.filter(username=self.cleaned_data['username']).count()
        if n == 0:
            return self.cleaned_data['username']
        else:
            raise forms.ValidationError(_T("The user name was used by someone else!"))

    def clean_email(self):
        n = User.objects.filter(email=self.cleaned_data['email']).count()
        if n < MAX_USER_PER_EMAIL:
            return self.cleaned_data['email']
        else:
            raise forms.ValidationError(_T("The email was used by someone else!"))

    def clean_password2(self):
        if self.cleaned_data['password2'] == self.cleaned_data['password1']:
            return self.cleaned_data['email']
        else:
            raise forms.ValidationError(_T("You should input two same passwords!"))
    
    def clean_validation(self):
        if self.code == "":
            raise forms.ValidationError(_T("The validation code has expired!"))
        elif self.cleaned_data['validation'] != self.code:
            raise forms.ValidationError(_T("Invalid validation code!"))
        else:
            return self.cleaned_data['validation']
