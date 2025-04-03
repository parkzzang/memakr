# common/image_utils.py

from PIL import Image, ImageDraw, ImageFont
import uuid
from datetime import datetime

def generate_unique_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    filename = f"output_{timestamp}_{unique_id}.png"
    return filename


def skew_image(image, skew_factor=0.5, direction='horizontal', left=True):
    width, height = image.size

    if direction == 'horizontal':
        xshift = int(abs(skew_factor) * height)
        padded = Image.new("RGBA", (width + 2 * xshift, height), (0, 0, 0, 0))
        paste_x = xshift if left else 0
        padded.paste(image, (paste_x, 0))

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


def draw_justified_text_in_box(image, text, box, font_path, max_font_size=60, fill='black'):
    x1, y1, x2, y2 = box
    max_width = x2 - x1
    max_height = y2 - y1
    draw = ImageDraw.Draw(image)

    font_size = max_font_size
    while font_size > 20:
        font = ImageFont.truetype(font_path, font_size)
        lines = wrap_text(draw, text, font, max_width)
        line_height = get_line_height(draw, font)
        total_height = len(lines) * line_height

        if total_height <= max_height:
            break
        font_size -= 15

    y = y1 + (max_height - total_height) // 2
    for line in lines:
        line = line.strip()
        if not line:
            continue
        line_width = draw.textlength(line, font=font)
        x = x1 + (max_width - line_width) // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height


def get_line_height(draw, font):
    bbox = draw.textbbox((0, 0), '가', font=font)
    return bbox[3] - bbox[1] + 8


def wrap_text(draw, text, font, max_width):
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
