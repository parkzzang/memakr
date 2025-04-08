from django import forms

class BlingForm(forms.Form):
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

    overlay_image = forms.ImageField(
        required=False,
        label='드레이크 몸통 이미지 업로드',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )