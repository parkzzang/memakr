from django import forms

class WoofForm(forms.Form):
    text = forms.CharField(
        max_length=100,
        required=False,
        label='문구 입력',
        widget=forms.TextInput(attrs={
            'placeholder': '',
            'class': 'form-control'
        })
    )

    overlay_image_1 = forms.ImageField(
        required=False,
        label='당하는 편 이미지 업로드',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )

    overlay_image_2 = forms.ImageField(
        required=False,
        label='공격하는 강아지 머리 이미지 업로드',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )