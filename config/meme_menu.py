# config/meme_menu.py

MEME_MENU = [
    {
        'name': '나쁜답변 좋은답변 밈',
        'slug': 'woof',
        'image': 'base.png',
        'example': 'woof_example.png',
    },
    {
        'name': '드레이크 거부/수용 밈',
        'slug': 'bling',
        'image': 'bling.png',
        'example': 'bling_example.png',
    },
    {
        'name': '용 3마리 밈',
        'slug': 'dragon',
        'image': 'dragon.jpg',
        'example': 'dragon_example.png',
    },
    {
        'name': '이겨야 한다/딸깍 밈',
        'slug': 'ddal',
        'image': 'ddal.png',
        'example': 'ddal_example.png',
    },
]

def get_meme_title(slug):
    for item in MEME_MENU:
        if item['slug'] == slug:
            return item['name']
    return '기본 제목'
