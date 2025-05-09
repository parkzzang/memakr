from django.urls import path
from .views import QuestionListView, QuestionDetailView
from . import views

app_name = 'community'

urlpatterns = [
    path('', QuestionListView.as_view(), name='index'),
    path('<int:pk>/', QuestionDetailView.as_view(), name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
    path('question/vote/<int:question_id>/', views.question_vote, name='question_vote'),
]
