from django import forms
from community.models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # 사용할 모델
        fields = ['subject', 'content', 'image']  # QuestionForm에서 사용할 Question 모델의 속성
        labels = {
            'subject': '제목',
            'content': '내용',
            'image': '이미지',
        }  

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '댓글 내용',
        }
