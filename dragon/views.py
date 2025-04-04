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
            text_3 = form.cleaned_data.get('text_3', '')
            image_1 = form.cleaned_data.get('image_1')
            image_2 = form.cleaned_data.get('image_2')
            image_3 = form.cleaned_data.get('image_3')

            # 기본 배경 이미지
            base_path = os.path.join(settings.BASE_DIR, 'static/dragon.jpg')
            base = Image.open(base_path).convert('RGBA')

            font_path = os.path.join(settings.BASE_DIR, 'static/fonts/NotoSansKR-ExtraBold.ttf')

            # ✅ image_1
            if image_1:
                try:
                    overlay = Image.open(image_1).convert("RGBA")
                    overlay = ImageOps.exif_transpose(overlay)
                    overlay.thumbnail((200, 200), Image.LANCZOS)
                    94,417,65
                    base.paste(overlay, (105 - overlay.width // 2, 440 - overlay.height // 2), overlay)
                except Exception as e:
                    print(f"image_1 처리 오류: {e}")

            # ✅ image_2
            if image_2:
                try:
                    overlay = Image.open(image_2).convert("RGBA")
                    overlay = ImageOps.exif_transpose(overlay)
                    overlay.thumbnail((200, 200), Image.LANCZOS)
                    base.paste(overlay, (330 - overlay.width // 2, 390 - overlay.height // 2), overlay)
                except Exception as e:
                    print(f"image_2 처리 오류: {e}")

            # ✅ image_3
            if image_3:
                try:
                    overlay = Image.open(image_3).convert("RGBA")
                    overlay = ImageOps.exif_transpose(overlay)
                    overlay.thumbnail((200, 200), Image.LANCZOS)
                    base.paste(overlay, (570 - overlay.width // 2, 430 - overlay.height // 2), overlay)
                except Exception as e:
                    print(f"image_3 처리 오류: {e}")

            # ✅ 텍스트들
            try:
                if text_1:
                    draw_justified_text_in_box(base, text_1, (83,28,175,90), font_path, max_font_size=60, fill='white')
                if text_2:
                    draw_justified_text_in_box(base, text_2, (297,10,389,72), font_path, max_font_size=60, fill='white')
                if text_3:
                    draw_justified_text_in_box(base, text_3, (506,27,598,89), font_path, max_font_size=60, fill='white')
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

    title = get_meme_title('dragon')  # 또는 request.path에서 앱 이름 자동 추출
    return render(request, 'dragon/index.html', {
        'form': form,
        'title': title
    })


# result 뷰
def result(request):
    image_path = request.session.get('generated_image')
    return render(request, 'result.html', {
        'image_path': image_path,
        'back_url': '/dragon/'
    })