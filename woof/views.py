from django.shortcuts import render
from common.views_base import meme_index_view
from .forms import WoofForm
from common.utils import (
    generate_unique_filename,
    skew_image,
    draw_justified_text_in_box,
)
from PIL import Image, ImageOps
import os
from django.conf import settings

def index(request):
    return meme_index_view(
        request=request,
        slug='woof',
        form_class=WoofForm,
        image_generation_logic=generate_woof_image,
        template_name='woof/landing.html',
        result_redirect_url='woof:result',
    )

def result(request):
    image_path = request.session.get('generated_image')
    return render(request, 'result.html', {
        'image_path': image_path,
        'back_url': '/woof/',
    })

# 이 함수는 woof/views.py 안에 그대로 둔다!
def generate_woof_image(form):
    text = form.cleaned_data['text']
    overlay_image_1 = form.cleaned_data['overlay_image_1']
    overlay_image_2 = form.cleaned_data['overlay_image_2']

    if overlay_image_1:
        base_path = os.path.join(settings.BASE_DIR, 'static/base2.png')
    else:
        base_path = os.path.join(settings.BASE_DIR, 'static/base.png')

    base = Image.open(base_path).convert('RGBA')

    # 이미지 합성 (앱 전용 로직)
    if overlay_image_1:
        overlay = Image.open(overlay_image_1).convert("RGBA")
        overlay = ImageOps.exif_transpose(overlay)
        overlay.thumbnail((250, 180), Image.LANCZOS)
        position1 = (135 - int(overlay.width / 2), 435 - int(overlay.height / 2))
        base.paste(overlay, position1, overlay)

        blurred = skew_image(overlay, skew_factor=0.7, direction='horizontal', left=True)
        position2 = (160 - int(blurred.width / 2), 1000 - int(blurred.height / 2))
        base.paste(blurred, position2, blurred)

    if overlay_image_2:
        overlay = Image.open(overlay_image_2).convert("RGBA")
        overlay = ImageOps.exif_transpose(overlay)
        overlay.thumbnail((160, 105), Image.LANCZOS)
        overlay = overlay.rotate(-10, expand=True)
        position1 = (440 - int(overlay.width / 2), 320 - int(overlay.height / 2))
        position2 = (460 - int(overlay.width / 2), 850 - int(overlay.height / 2))
        base.paste(overlay, position1, overlay)
        base.paste(overlay, position2, overlay)

    if text:
        font_path = os.path.join(settings.BASE_DIR, 'static/fonts/NotoSansKR-ExtraBold.ttf')
        draw_justified_text_in_box(base, text, (15, 130, 260, 295), font_path, max_font_size=39, fill='black')
        draw_justified_text_in_box(base, text, (15, 687, 260, 852), font_path, max_font_size=39, fill='black')

    filename = generate_unique_filename()
    output_path = os.path.join(settings.MEDIA_ROOT, filename)
    base.save(output_path)
    return os.path.join(settings.MEDIA_URL, filename)
