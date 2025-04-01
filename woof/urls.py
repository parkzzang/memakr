from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('result/', views.result, name='result'),  # ← 여기 추가
]