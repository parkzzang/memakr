from django.shortcuts import render, redirect
from common.favorites import get_meme_by_slug, is_favorited_by_user

def meme_index_view(request, *, slug, form_class, image_generation_logic, template_name, result_redirect_url):
    meme = get_meme_by_slug(slug)
    title = meme['name'] if meme else '기본 제목'

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            # 앱마다 다른 이미지 생성 로직을 여기서 실행
            image_url = image_generation_logic(form)
            request.session['generated_image'] = image_url
            return redirect(result_redirect_url)
    else:
        form = form_class()

    is_favorited = is_favorited_by_user(request.user, slug)

    return render(request, template_name, {
        'form': form,
        'title': title,
        'slug': slug,
        'is_favorited': is_favorited,
    })
