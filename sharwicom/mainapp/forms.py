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

class ContentForm(forms.Form):
    CONTENT_TYPES = [
        ('book', 'Book'),
        ('movie', 'Movie'),
        ('song', 'Song'),
        ('album', 'Album'),
        ('video', 'Video'),
        ('other', 'Other')
    ]

    title = forms.CharField(max_length=50, label="Content's title")
    author = forms.CharField(max_length=100, label="Content's author")
    type = forms.ChoiceField(choices=CONTENT_TYPES, label="Content's type")
    description = forms.CharField(widget=forms.Textarea, label="Content's description")
    captcha = CaptchaField()

class ReviewForm(forms.Form):
    summary = forms.CharField(max_length=50, label="Review summary")
    description = forms.CharField(widget=forms.Textarea, label="Review description")
    captcha = CaptchaField()
