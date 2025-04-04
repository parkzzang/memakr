from django.shortcuts import render, redirect
from .forms import ImageForm
from PIL import Image, ImageOps
import os
from django.conf import settings
from config.meme_menu import get_meme_title

from common.utils import (
    generate_unique_filename,
    skew_image,
    draw_justified_text_in_box,
)

# index 뷰
def index(request):
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data['text']
            overlay_image_1 = form.cleaned_data['overlay_image_1']
            overlay_image_2 = form.cleaned_data['overlay_image_2']

            # 조건에 따라 base 이미지 선택
            if overlay_image_1:
                base_path = os.path.join(settings.BASE_DIR, 'static/base2.png')
            else:
                base_path = os.path.join(settings.BASE_DIR, 'static/base.png')

            base = Image.open(base_path).convert('RGBA')


            # 업로드된 이미지 삽입

            if overlay_image_1:
                overlay = Image.open(overlay_image_1).convert("RGBA")
                overlay = ImageOps.exif_transpose(overlay)

                # 비율 유지하며 축소
                overlay.thumbnail((250, 180), Image.LANCZOS)

                # 첫 번째 삽입 (중앙)
                position1 = (135 - int(overlay.width / 2), 435 - int(overlay.height / 2))
                base.paste(overlay, position1, overlay)

                # 두 번째 삽입: 회전 + 블러
                blurred = skew_image(overlay, skew_factor=0.7, direction='horizontal', left=True)

                # 삽입 위치 아래쪽
                position2 = (160 - int(blurred.width / 2), 1000 - int(blurred.height / 2))
                base.paste(blurred, position2, blurred)

            if overlay_image_2:
                overlay = Image.open(overlay_image_2).convert("RGBA")
                overlay = ImageOps.exif_transpose(overlay)

                # 비율 유지하며 축소
                overlay.thumbnail((160, 105), Image.LANCZOS)

                # 첫 번째 삽입 (중앙)
                overlay = overlay.rotate(-10, expand=True)
                position1 = (440 - int(overlay.width / 2), 320 - int(overlay.height / 2))
                base.paste(overlay, position1, overlay)

                # 두 번째 삽입
                position2 = (460 - int(overlay.width / 2), 850 - int(overlay.height / 2))
                base.paste(overlay, position2, overlay)

            # 텍스트 양쪽정렬로 삽입
            if text:
                font_path = os.path.join(settings.BASE_DIR, 'static/fonts/NotoSansKR-ExtraBold.ttf')
                text_box_1 = (15, 130, 260, 295)  # (x1, y1, x2, y2)
                text_box_2 = (15, 687, 260, 852)  # (x1, y1, x2, y2)
                draw_justified_text_in_box(base, text, text_box_1, font_path, max_font_size=39, fill='black')
                draw_justified_text_in_box(base, text, text_box_2, font_path, max_font_size=39, fill='black')

            # 저장
            filename = generate_unique_filename()
            output_path = os.path.join(settings.MEDIA_ROOT, filename)
            base.save(output_path)
            request.session['generated_image'] = os.path.join(settings.MEDIA_URL, filename)
            return redirect('woof:result')
    else:
        form = ImageForm()

    title = get_meme_title('woof')  # 또는 request.path에서 앱 이름 자동 추출
    return render(request, 'woof/landing.html', {
        'form': form,
        'title': title
    })

# result 뷰
def result(request):
    image_path = request.session.get('generated_image')
    return render(request, 'result.html', {
        'image_path': image_path,
        'back_url': '/woof/'
    })