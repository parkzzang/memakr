from django import forms

class WorldForm(forms.Form):
    text_1 = forms.CharField(
        max_length=100,
        required=False,
        label='문구 입력',
        widget=forms.TextInput(attrs={
            'placeholder': '',
            'class': 'form-control'
        })
    )

    text_2 = forms.CharField(
        max_length=100,
        required=False,
        label='문구 입력',
        widget=forms.TextInput(attrs={
            'placeholder': '',
            'class': 'form-control'
        })
    )

    image_1 = forms.ImageField(
        required=False,
        label='이미지 업로드',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )