from django import forms

class ImageForm(forms.Form):
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
        label='겹쳐넣을 이미지 업로드',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )

    overlay_image_2 = forms.ImageField(
        required=False,
        label='겹쳐넣을 이미지 업로드',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )