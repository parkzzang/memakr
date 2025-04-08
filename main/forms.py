from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    agree_terms = forms.BooleanField(required=True, label="이용약관 동의")
    agree_privacy = forms.BooleanField(required=True, label="개인정보처리방침 동의")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

    def clean(self):
        cleaned_data = super().clean()