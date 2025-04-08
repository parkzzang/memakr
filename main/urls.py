# main/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='main'

urlpatterns = [
    path('', views.home, name='home'),  # 메인 페이지
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('favorite/<slug:slug>/', views.toggle_favorite, name='toggle_favorite'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
]
