from django.shortcuts import render
from PIL import Image, ImageOps
import os
from django.conf import settings

from .forms import DdalForm
from common.utils import (
    generate_unique_filename,
    draw_justified_text_in_box,
)
from common.views_base import meme_index_view


# 🧠 index 뷰 - 공통 처리 + 이미지 생성 함수 사용
def index(request):
    return meme_index_view(
        request=request,
        slug='ddal',
        form_class=DdalForm,
        image_generation_logic=generate_ddal_image,
        template_name='ddal/index.html',
        result_redirect_url='ddal:result',
    )


# 🎯 result 뷰
def result(request):
    image_path = request.session.get('generated_image')
    return render(request, 'result.html', {
        'image_path': image_path,
        'back_url': '/ddal/',
    })


# 🎨 이미지 생성 함수 (앱 안에 유지)
def generate_ddal_image(form):
    text_1 = form.cleaned_data.get('text_1', '')
    text_2 = form.cleaned_data.get('text_2', '')
    image_1 = form.cleaned_data.get('image_1')
    image_2 = form.cleaned_data.get('image_2')

    base_path = os.path.join(settings.BASE_DIR, 'static/ddal.png')
    base = Image.open(base_path).convert('RGBA')
    font_path = os.path.join(settings.BASE_DIR, 'static/fonts/NotoSansKR-ExtraBold.ttf')

    if image_1:
        try:
            overlay = Image.open(image_1).convert("RGBA")
            overlay = ImageOps.exif_transpose(overlay)
            overlay.thumbnail((150, 150), Image.LANCZOS)
            base.paste(overlay, (200 - overlay.width // 2, 335 - overlay.height // 2), overlay)
        except Exception as e:
            print(f"image_1 처리 오류: {e}")

    if image_2:
        try:
            overlay = Image.open(image_2).convert("RGBA")
            overlay = ImageOps.exif_transpose(overlay)
            overlay.thumbnail((150, 150), Image.LANCZOS)
            rotated_overlay = overlay.rotate(-20, expand=True)
            base.paste(rotated_overlay, (850 - overlay.width // 2, 300 - overlay.height // 2), rotated_overlay)
        except Exception as e:
            print(f"image_2 처리 오류: {e}")

    try:
        if text_1:
            draw_justified_text_in_box(base, text_1, (6, 621, 481, 740), font_path, max_font_size=60, fill='red')
        if text_2:
            draw_justified_text_in_box(base, text_2, (507, 625, 982, 744), font_path, max_font_size=60, fill='red')
    except Exception as e:
        print(f"텍스트 처리 오류: {e}")

    filename = generate_unique_filename()
    output_path = os.path.join(settings.MEDIA_ROOT, filename)
    base.save(output_path)
    return os.path.join(settings.MEDIA_URL, filename)
