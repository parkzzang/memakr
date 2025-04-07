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

def index(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # 텍스트 & 이미지 받아오기
            text_1 = form.cleaned_data.get('text_1', '')
            text_2 = form.cleaned_data.get('text_2', '')
            image_1 = form.cleaned_data.get('image_1')
            image_2 = form.cleaned_data.get('image_2')

            # 기본 배경 이미지
            base_path = os.path.join(settings.BASE_DIR, 'static/ddal.png')
            base = Image.open(base_path).convert('RGBA')

            font_path = os.path.join(settings.BASE_DIR, 'static/fonts/NotoSansKR-ExtraBold.ttf')

            # ✅ image_1
            if image_1:
                try:
                    overlay = Image.open(image_1).convert("RGBA")
                    overlay = ImageOps.exif_transpose(overlay)
                    overlay.thumbnail((150, 150), Image.LANCZOS)
                    base.paste(overlay, (200 - overlay.width // 2, 335 - overlay.height // 2), overlay)
                except Exception as e:
                    print(f"image_1 처리 오류: {e}")

            # ✅ image_2
            if image_2:
                try:
                    overlay = Image.open(image_2).convert("RGBA")
                    overlay = ImageOps.exif_transpose(overlay)
                    overlay.thumbnail((150, 150), Image.LANCZOS)
                    #회전 후 삽입
                    rotated_overlay = overlay.rotate(-20, expand=True)
                    base.paste(rotated_overlay, (850 - overlay.width // 2, 300 - overlay.height // 2), rotated_overlay)
                except Exception as e:
                    print(f"image_2 처리 오류: {e}")

            # ✅ 텍스트들
            try:
                if text_1:
                    draw_justified_text_in_box(base, text_1, (6,621,481,740), font_path, max_font_size=60, fill='red')
                if text_2:
                    draw_justified_text_in_box(base, text_2, (507,625,982,744), font_path, max_font_size=60, fill='red')
            except Exception as e:
                print(f"텍스트 처리 오류: {e}")

            # 저장
            filename = generate_unique_filename()
            output_path = os.path.join(settings.MEDIA_ROOT, filename)
            base.save(output_path)
            request.session['generated_image'] = os.path.join(settings.MEDIA_URL, filename)

            return redirect('dragon:result')
    else:
        form = ImageForm()

    title = get_meme_title('ddal')  # 또는 request.path에서 앱 이름 자동 추출
    return render(request, 'ddal/index.html', {
        'form': form,
        'title': title
    })


# result 뷰
def result(request):
    image_path = request.session.get('generated_image')
    return render(request, 'result.html', {
        'image_path': image_path,
        'back_url': '/ddal/'
    })