from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AbstractUser
from main.forms import UserForm
from .models import UserFavorite
from config.meme_menu import MEME_MENU

def home(request):
    return render(request, 'main/home.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'main/signup.html', {'form': form})

def page_not_found(request, exception):
    return render(request, 'main/404.html', {})

@login_required(login_url='main:login')
def toggle_favorite(request, slug):
    favorite, created = UserFavorite.objects.get_or_create(
        user=request.user, template_slug=slug
    )
    if not created:
        favorite.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def my_favorites(request):
    # 현재 유저가 찜한 slug 목록
    favorite_slugs = UserFavorite.objects.filter(user=request.user).values_list('template_slug', flat=True)

    # MEME_MENU에서 해당 slug만 추출
    favorite_memes = [meme for meme in MEME_MENU if meme['slug'] in favorite_slugs]

    return render(request, 'main/my_favorites.html', {
        'favorites': favorite_memes
    })