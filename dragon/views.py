from django.shortcuts import render
from PIL import Image, ImageOps
import os
from django.conf import settings

from .forms import DragonForm
from common.utils import (
    generate_unique_filename,
    draw_justified_text_in_box,
)
from common.views_base import meme_index_view


# 🧠 index 뷰: 공통 처리 + 이미지 생성 로직
def index(request):
    return meme_index_view(
        request=request,
        slug='dragon',
        form_class=DragonForm,
        image_generation_logic=generate_dragon_image,
        template_name='dragon/index.html',
        result_redirect_url='dragon:result'
    )


# 🎯 결과 페이지
def result(request):
    image_path = request.session.get('generated_image')
    return render(request, 'result.html', {
        'image_path': image_path,
        'back_url': '/dragon/',
    })


# 🎨 이미지 생성 함수 (앱 내부에 유지)
def generate_dragon_image(form):
    # 텍스트 & 이미지 받아오기
    text_1 = form.cleaned_data.get('text_1', '')
    text_2 = form.cleaned_data.get('text_2', '')
    text_3 = form.cleaned_data.get('text_3', '')
    image_1 = form.cleaned_data.get('image_1')
    image_2 = form.cleaned_data.get('image_2')
    image_3 = form.cleaned_data.get('image_3')

    # 배경 이미지
    base_path = os.path.join(settings.BASE_DIR, 'static/dragon.jpg')
    base = Image.open(base_path).convert('RGBA')
    font_path = os.path.join(settings.BASE_DIR, 'static/fonts/NotoSansKR-ExtraBold.ttf')

    # 이미지 삽입
    if image_1:
        try:
            overlay = Image.open(image_1).convert("RGBA")
            overlay = ImageOps.exif_transpose(overlay)
            overlay.thumbnail((200, 200), Image.LANCZOS)
            base.paste(overlay, (105 - overlay.width // 2, 440 - overlay.height // 2), overlay)
        except Exception as e:
            print(f"image_1 처리 오류: {e}")

    if image_2:
        try:
            overlay = Image.open(image_2).convert("RGBA")
            overlay = ImageOps.exif_transpose(overlay)
            overlay.thumbnail((200, 200), Image.LANCZOS)
            base.paste(overlay, (330 - overlay.width // 2, 390 - overlay.height // 2), overlay)
        except Exception as e:
            print(f"image_2 처리 오류: {e}")

    if image_3:
        try:
            overlay = Image.open(image_3).convert("RGBA")
            overlay = ImageOps.exif_transpose(overlay)
            overlay.thumbnail((200, 200), Image.LANCZOS)
            base.paste(overlay, (570 - overlay.width // 2, 430 - overlay.height // 2), overlay)
        except Exception as e:
            print(f"image_3 처리 오류: {e}")

    # 텍스트 삽입
    try:
        if text_1:
            draw_justified_text_in_box(base, text_1, (83, 28, 175, 90), font_path, max_font_size=60, fill='white')
        if text_2:
            draw_justified_text_in_box(base, text_2, (297, 10, 389, 72), font_path, max_font_size=60, fill='white')
        if text_3:
            draw_justified_text_in_box(base, text_3, (506, 27, 598, 89), font_path, max_font_size=60, fill='white')
    except Exception as e:
        print(f"텍스트 처리 오류: {e}")

    # 저장
    filename = generate_unique_filename()
    output_path = os.path.join(settings.MEDIA_ROOT, filename)
    base.save(output_path)
    return os.path.join(settings.MEDIA_URL, filename)
