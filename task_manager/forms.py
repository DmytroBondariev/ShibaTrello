from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, \
    PasswordChangeForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Username"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "Password"}),
    )


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Email'
    }))


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Old Password'
    }), label="New Password")
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")


class WorkerSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name.."})
    )


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name.."})
    )
