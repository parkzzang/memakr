from django.shortcuts import render, redirect
from .forms import ImageForm
from PIL import Image, ImageDraw, ImageFont
import os, uuid
from django.conf import settings
from datetime import datetime

def generate_unique_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    filename = f"output_{timestamp}_{unique_id}.png"
    return filename

# 기울이기(평행사변형) 효과 함수
def skew_image(image, skew_factor=0.5, direction='horizontal', left=True):
    width, height = image.size

    if direction == 'horizontal':
        xshift = int(abs(skew_factor) * height)

        # ✅ 왼쪽, 오른쪽 여백 모두 확보
        padded = Image.new("RGBA", (width + 2 * xshift, height), (0, 0, 0, 0))
        
        # 왼쪽으로 기울일 경우: 중앙에 붙여서 왼쪽 공간 확보
        paste_x = xshift if left else 0
        padded.paste(image, (paste_x, 0))

        # 변형 후에도 오른쪽이 잘리지 않도록 전체 크기로 transform
        coeffs = (
            1, -skew_factor if left else skew_factor, xshift if left else 0,
            0, 1, 0
        )

        return padded.transform(padded.size, Image.Transform.AFFINE, coeffs, Image.Resampling.BICUBIC)

    elif direction == 'vertical':
        yshift = int(abs(skew_factor) * width)
        padded = Image.new("RGBA", (width, height + 2 * yshift), (0, 0, 0, 0))

        paste_y = yshift if left else 0
        padded.paste(image, (0, paste_y))

        coeffs = (
            1, 0, 0,
            -skew_factor if left else skew_factor, 1, yshift if left else 0
        )

        return padded.transform(padded.size, Image.Transform.AFFINE, coeffs, Image.Resampling.BICUBIC)


# -------------------------------
# 양쪽 정렬 함수 + 텍스트 줄바꿈
# -------------------------------

def draw_justified_text_in_box(image, text, box, font_path, max_font_size=60, fill='black'):
    """
    Pillow 최신 스타일로 특정 사각형 영역에 텍스트를 양쪽정렬로 출력하는 함수
    :param image: PIL.Image 객체
    :param text: 출력할 문자열
    :param box: (x1, y1, x2, y2) 사각형 영역
    :param font_path: 사용할 폰트 경로 (.ttf 또는 .otf)
    :param max_font_size: 최대 폰트 크기
    :param fill: 텍스트 색상
    """
    x1, y1, x2, y2 = box
    max_width = x2 - x1
    max_height = y2 - y1
    draw = ImageDraw.Draw(image)

    # 텍스트박스 위치 확인 코드 draw.rectangle(box, outline='red', width=2)

    # 1. 폰트 크기 자동 조절
    font_size = max_font_size
    while font_size > 20:
        font = ImageFont.truetype(font_path, font_size)
        lines = wrap_text(draw, text, font, max_width)
        line_height = get_line_height(draw, font)
        total_height = len(lines) * line_height

        if total_height <= max_height:
            break
        font_size -= 15

    # 2. 줄 단위로 양쪽 정렬 텍스트 출력
    # 세로 가운데 정렬 시작 y 위치
    y = y1 + (max_height - total_height) // 2
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        line_width = draw.textlength(line, font=font)
        x = x1 + (max_width - line_width) // 2  # ← 가운데 정렬 포인트
    
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height

def get_line_height(draw, font):
    """
    한 줄 높이 계산 (Pillow 최신 방식)
    """
    bbox = draw.textbbox((0, 0), '가', font=font)
    return bbox[3] - bbox[1] + 8  # 여백 포함

def wrap_text(draw, text, font, max_width):
    """
    사각형 너비에 맞게 줄바꿈된 텍스트 리스트 반환
    """
    lines = []
    for paragraph in text.split('\n'):
        line = ''
        for word in paragraph.split():
            test_line = line + ' ' + word if line else word
            width = draw.textlength(test_line, font=font)
            if width <= max_width:
                line = test_line
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines

# -------------------------------
# index 뷰
# -------------------------------
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

                # 비율 유지하며 축소
                overlay.thumbnail((150, 80), Image.LANCZOS)

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
            return redirect('result')
    else:
        form = ImageForm()

    return render(request, 'woof/landing.html', {'form': form})

# -------------------------------
# result 뷰
# -------------------------------
def result(request):
    image_path = request.session.get('generated_image')
    return render(request, 'woof/result.html', {'image_path': image_path})
