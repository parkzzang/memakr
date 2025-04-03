from config.meme_menu import MEME_MENU

def meme_menu(request):
    return {
        'meme_menu': MEME_MENU
    }
