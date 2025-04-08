from config.meme_menu import MEME_MENU
from main.models import UserFavorite

def get_meme_by_slug(slug):
    return next((m for m in MEME_MENU if m['slug'] == slug), None)

def is_favorited_by_user(user, slug):
    if user.is_authenticated:
        return UserFavorite.objects.filter(user=user, template_slug=slug).exists()
    return False

def get_user_favorites(user):
    slugs = UserFavorite.objects.filter(user=user).values_list('template_slug', flat=True)
    return [m for m in MEME_MENU if m['slug'] in slugs]
