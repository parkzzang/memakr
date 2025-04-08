from django.shortcuts import render
from config.meme_menu import get_meme_title
from .forms import BlingForm
from PIL import Image, ImageOps
import os
from django.conf import settings
from common.utils import (
    generate_unique_filename,
    draw_justified_text_in_box,
)
from common.views_base import meme_index_view
from common.favorites import is_favorited_by_user


# 🧠 index 뷰: 공통 흐름 + 이미지 생성 콜백 함수 사용
def index(request):
    return meme_index_view(
        request=request,
        slug='bling',
        form_class=BlingForm,
        image_generation_logic=generate_bling_image,
        template_name='bling/landing.html',
        result_redirect_url='bling:result'
    )


# 🖼️ 결과 페이지
def result(request):
    image_path = request.session.get('generated_image')
    return render(request, 'result.html', {
        'image_path': image_path,
        'back_url': '/bling/',
    })


# 🎨 이미지 생성 로직은 각 앱에 남겨두기 (원본 그대로)
def generate_bling_image(form):
    text_1 = form.cleaned_data['text_1']
    text_2 = form.cleaned_data['text_2']
    overlay_image = form.cleaned_data['overlay_image']

    base_path = os.path.join(settings.BASE_DIR, 'static/bling.png')
    base = Image.open(base_path).convert('RGBA')

    # 이미지 삽입
    if overlay_image:
        overlay = Image.open(overlay_image).convert("RGBA")
        overlay = ImageOps.exif_transpose(overlay)
        overlay.thumbnail((200, 200), Image.LANCZOS)

        rotated_overlay = overlay.rotate(10, expand=True)
        position1 = (270 - int(rotated_overlay.width / 2), 420 - int(rotated_overlay.height / 2))
        base.paste(rotated_overlay, position1, rotated_overlay)

        position2 = (240 - int(overlay.width / 2), 950 - int(overlay.height / 2))
        base.paste(overlay, position2, overlay)

    # 텍스트 삽입
    font_path = os.path.join(settings.BASE_DIR, 'static/fonts/NotoSansKR-ExtraBold.ttf')
    if text_1:
        text_box_1 = (540, 0, 1080, 540)
        draw_justified_text_in_box(base, text_1, text_box_1, font_path, max_font_size=70, fill='black')

    if text_2:
        text_box_2 = (540, 540, 1080, 1080)
        draw_justified_text_in_box(base, text_2, text_box_2, font_path, max_font_size=70, fill='black')

    # 저장
    filename = generate_unique_filename()
    output_path = os.path.join(settings.MEDIA_ROOT, filename)
    base.save(output_path)
    return os.path.join(settings.MEDIA_URL, filename)
