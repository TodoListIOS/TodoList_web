from django import forms
from captcha.fields import CaptchaField
from django.db import models
from django.forms import ModelForm


class LoginForm(forms.Form):
    email = forms.CharField(label="Email", max_length=128,
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='Captcha  ')


class RegisterForm(forms.Form):
    username = forms.CharField(label="Username:", max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password:", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confine Password:", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='Captcha  ')


class FeedBack(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'style': 'height: 120px;width:100%'}))


class PwdBack(forms.Form):
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))


class AuthCode(forms.Form):
    AuthCode = forms.CharField(label="AuthCode:", max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="New Password:", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confine Password:", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ItemForm(forms.Form):
    Title = forms.CharField(label="Title：", max_length=128,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    DueDate = forms.DateTimeField(label="DueDate:", widget=forms.DateInput(attrs={'type': 'date'}))


class UserChangeForm(forms.Form):
    username = forms.CharField(label="Username:", max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password0 = forms.CharField(label="Original Password:", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="New Password:", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confine Password:", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='Captcha  ')


class ChangeRecord(forms.Form):
    title = forms.CharField(label="Title：", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    DueDate = forms.DateTimeField(label="DueDate:", widget=forms.DateInput(attrs={'type': 'date'}))
