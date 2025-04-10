from django.shortcuts import render
from PIL import Image, ImageOps, ImageDraw
import os
from django.conf import settings

from .forms import WorldForm
from common.utils import (
    generate_unique_filename,
    draw_justified_text_in_box,
)
from common.views_base import meme_index_view


# 🧠 index 뷰 - 공통 처리 + 이미지 생성 함수 사용
def index(request):
    return meme_index_view(
        request=request,
        slug='world',
        form_class=WorldForm,
        image_generation_logic=generate_world_image,
        template_name='world/index.html',
        result_redirect_url='world:result',
    )


# 🎯 result 뷰
def result(request):
    image_path = request.session.get('generated_image')
    return render(request, 'result.html', {
        'image_path': image_path,
        'back_url': '/world/',
    })


# 🎨 이미지 생성 함수 (앱 안에 유지)
def generate_world_image(form):
    text_1 = form.cleaned_data.get('text_1', '')
    text_2 = form.cleaned_data.get('text_2', '')
    image_1 = form.cleaned_data.get('image_1')

    base_path = os.path.join(settings.BASE_DIR, 'static/world.png')
    base = Image.open(base_path).convert('RGBA')
    font_path = os.path.join(settings.BASE_DIR, 'static/fonts/NotoSerifKR-ExtraBold.ttf')

    if image_1:
        try:
            overlay = Image.open(image_1).convert("RGBA")
            overlay = ImageOps.exif_transpose(overlay)

            # ⬇️ 비율 유지하면서 (1592, 1140)에 맞게 꽉 채우도록 강제 크기 조정
            overlay = ImageOps.fit(overlay, (635, 460), method=Image.LANCZOS)

            base.paste(overlay, (0, 0), overlay)
        except Exception as e:
            print(f"image_1 처리 오류: {e}")

    try:
        if text_1:
            text_box_1 = (38, 580, 514, 692)
            draw_justified_text_in_box(base, text_1, text_box_1, font_path, max_font_size=60)
        if text_2:
            text_box_2 = (48, 760, 474, 800)
            draw_justified_text_in_box(base, text_2, text_box_2, font_path, max_font_size=25, align='left')


    except Exception as e:
        print(f"텍스트 처리 오류: {e}")

    filename = generate_unique_filename()
    output_path = os.path.join(settings.MEDIA_ROOT, filename)
    base.save(output_path)
    return os.path.join(settings.MEDIA_URL, filename)
