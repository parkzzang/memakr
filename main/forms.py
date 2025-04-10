from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # ← 사용자 정의 유저 모델을 import


class UserForm(UserCreationForm):
    agree_terms = forms.BooleanField(required=True, label="이용약관 동의")
    agree_privacy = forms.BooleanField(required=True, label="개인정보처리방침 동의")

    class Meta:
        model = CustomUser  # ← 여기서 기본 User 대신 CustomUser 사용
        fields = ("username", "password1", "password2")

    def clean(self):
        cleaned_data = super().clean()
        # 필요한 추가 검증 로직 여기에 추가
        return cleaned_data
