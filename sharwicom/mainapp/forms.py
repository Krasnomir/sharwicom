from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()
