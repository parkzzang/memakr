from django.shortcuts import render, redirect
from .forms import ImageForm
from PIL import Image, ImageOps
import os
from django.conf import settings
from config.meme_menu import get_meme_title

from common.utils import (
    generate_unique_filename,
    draw_justified_text_in_box,
)

# index 뷰
def index(request):
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            text_1 = form.cleaned_data['text_1']
            text_2 = form.cleaned_data['text_2']
            overlay_image = form.cleaned_data['overlay_image']

            base_path = os.path.join(settings.BASE_DIR, 'static/bling.png')

            base = Image.open(base_path).convert('RGBA')

            # 업로드된 이미지 삽입
            if overlay_image:
                overlay = Image.open(overlay_image).convert("RGBA")
                overlay = ImageOps.exif_transpose(overlay)

                # 비율 유지하며 축소
                overlay.thumbnail((200, 200), Image.LANCZOS)

                # ✅ 첫 번째 삽입용: 회전 처리 (예: 10도 회전)
                rotated_overlay = overlay.rotate(10, expand=True)
                position1 = (270 - int(rotated_overlay.width / 2), 420 - int(rotated_overlay.height / 2))
                base.paste(rotated_overlay, position1, rotated_overlay)

                # 두 번째 삽입은 그대로 사용
                position2 = (240 - int(overlay.width / 2), 950 - int(overlay.height / 2))
                base.paste(overlay, position2, overlay)

            # 텍스트 양쪽정렬로 삽입
            font_path = os.path.join(settings.BASE_DIR, 'static/fonts/NotoSansKR-ExtraBold.ttf')
            if text_1:
                text_box_1 = (540, 0, 1080, 540)  # (x1, y1, x2, y2)
                draw_justified_text_in_box(base, text_1, text_box_1, font_path, max_font_size=50, fill='black')
                
            if text_2:
                text_box_2 = (540, 540, 1080, 1080)  # (x1, y1, x2, y2)
                draw_justified_text_in_box(base, text_2, text_box_2, font_path, max_font_size=50, fill='black')

            # 저장
            filename = generate_unique_filename()
            output_path = os.path.join(settings.MEDIA_ROOT, filename)
            base.save(output_path)
            request.session['generated_image'] = os.path.join(settings.MEDIA_URL, filename)
            return redirect('bling:result')
    else:
        form = ImageForm()

    title = get_meme_title('bling')
    return render(request, 'bling/landing.html', {
        'form': form,
        'title': title
    })

# result 뷰
def result(request):
    image_path = request.session.get('generated_image')
    return render(request, 'result.html', {
        'image_path': image_path,
        'back_url': '/bling/'
    })