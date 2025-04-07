from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

class QuestionListView(ListView):
    model = Question
    ordering = ['-create_date']
    context_object_name = 'question_list'
    paginate_by = 10  # 선택사항: 페이지네이션

    def get_queryset(self):
        queryset = super().get_queryset()
        kw = self.request.GET.get('kw', '')
        if kw:
            queryset = queryset.filter(
                Q(subject__icontains=kw) |
                Q(content__icontains=kw) |
                Q(answer__content__icontains=kw)
            ).distinct()
        return queryset
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['kw'] = self.request.GET.get('kw', '')
         return context


class QuestionDetailView(DetailView):
    model = Question
    context_object_name = 'question'

@login_required(login_url='main:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('community:detail', pk=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'community/question_detail.html', context)

@login_required(login_url='main:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('community:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'community/question_form.html', context)

@login_required(login_url='main:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('community:detail', pk=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('community:detail', pk=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'community/question_form.html', context)

@login_required(login_url='main:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('community:detail', pk=question.id)
    question.delete()
    return redirect('community:index')

@login_required(login_url='main:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다.')
    else:
        answer.delete()
    return redirect('community:detail', pk=answer.question.id)

@login_required(login_url='main:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        question.voter.add(request.user)
    return redirect('community:detail', pk=question.id)