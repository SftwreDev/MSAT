from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from quiz.decorators import student_required, teacher_required
from exams.forms import BaseAnswerInlineFormSet, QuestionForm, TakeExamsForm, CreateExamForm, Year_LevelForm
from .models import Answer, Question
from quiz.models import Exams, TakenExams
from quiz.models import User
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.urls import reverse, reverse_lazy

from bootstrap_modal_forms.generic import (BSModalLoginView,
                                           BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)


 #                                       '''S    T   U   D   E   N   T   S'''




@method_decorator([login_required, student_required], name='dispatch')
class StudentsExamsListView(ListView):
    model = Exams
    ordering = ('name', )
    context_object_name = 'exams'
    template_name = 'classroom/students/exam_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_year_level = student.year_level.values_list('pk', flat=True)
        taken_exams = student.examinations.values_list('pk', flat=True)
        queryset = Exams.objects.filter(year_level__in=student_year_level) \
            .exclude(pk__in=taken_exams) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset

@method_decorator([login_required, student_required], name='dispatch')
class TakenExamsListView(ListView):
    model = TakenExams
    template_name = 'classroom/students/taken_exams_list.html'
    context_object_name = 'taken_exams'

    def get_queryset(self):
        queryset = self.request.user.student.taken_exams \
            .select_related('exams', 'exams__year_level') \
            .order_by('exams__name')
        return queryset


@login_required
@student_required
def take_exams(request, pk):
    exams = get_object_or_404(Exams, pk=pk)
    student = request.user.student

    if student.examinations.filter(pk=pk).exists():
        return render(request, 'classroom/students/taken_exams.html')

    total_questions = exams.questions.count()
    unanswered_questions = student.get_unanswered_exams(exams)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeExamsForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_exams(exams).exists():
                    return redirect('exams:take_exams_form', pk)
                else:
                    correct_answers = student.exams_answers.filter(answer__question__exams=exams, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenExams.objects.create(student=student, exams=exams, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (exams.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (exams.name, score))
                    return redirect('exams:exams_list')
    else:
        form = TakeExamsForm(question=question)

    return render(request, 'classroom/students/take_exams.html', {
        'exams': exams,
        'question': question,
        'form': form,
        'progress': progress
    })


#                                                    '''T    E   A   C   H   E   R   S'''




@method_decorator([login_required, teacher_required], name='dispatch')
class TeachersExamsListView(ListView):
    model = Exams
    ordering = ('name', )
    context_object_name = 'exams'
    template_name = 'classroom/teachers/exams_list.html'

    def get_queryset(self):
        queryset = self.request.user.exams \
            .select_related('owner') \
            .annotate(questions_count=Count('questions', distinct=True)) \
            .annotate(taken_count=Count('taken_exams', distinct=True))
        return queryset


@method_decorator([login_required, teacher_required], name='dispatch')
class ExamsCreateView(CreateView):
    model = Exams
    fields = ('name','year_level', )
    template_name = 'classroom/teachers/exams_add_form.html'

    def form_valid(self, form):
        exams = form.save(commit=False)
        exams.owner = self.request.user
        exams.save()
        messages.success(self.request, 'The exams was created with success! Go ahead and add some questions now.')
        return redirect('exams:update_exams', exams.pk)


@method_decorator([login_required, teacher_required], name='dispatch')
class ExamsUpdateView(UpdateView):
    model = Exams
    fields = ('name', )
    context_object_name = 'exams'
    template_name = 'classroom/teachers/exams_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.exams.all()

    def get_success_url(self):
        return reverse('exams:update_exams', kwargs={'pk': self.object.pk})


@method_decorator([login_required, teacher_required], name='dispatch')
class ExamsDeleteView(DeleteView):
    model = Exams
    context_object_name = 'exams'
    template_name = 'classroom/teachers/exams_delete_confirm.html'
    success_url = reverse_lazy('exams:created_exams_list')

    def delete(self, request, *args, **kwargs):
        exams = self.get_object()
        messages.success(request, 'The exams %s was deleted with success!' % exams.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.exams.all()


@method_decorator([login_required, teacher_required], name='dispatch')
class ExamsResultsView(DetailView):
    model = Exams
    context_object_name = 'exams'
    template_name = 'classroom/teachers/exams_results.html'

    def get_context_data(self, **kwargs):
        exams = self.get_object()
        taken_exams = exams.taken_exams.select_related('student__user').order_by('-date')
        total_taken_exams = taken_exams.count()
        exams_score = exams.taken_exams.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_exams': taken_exams,
            'total_taken_exams': total_taken_exams,
            'exams_score': exams_score
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.exams.all()


@login_required
@teacher_required
def exams_question_add(request, pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.
    exams = get_object_or_404(Exams, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exams = exams

            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('exams:exams_question_change', exams.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'classroom/teachers/exams_question_add_form.html', {'exams': exams, 'form': form})


@login_required
@teacher_required
def question_change(request, exams_pk, question_pk):
    # Simlar to the `question_add` view, this view is also managing
    # the permissions at object-level. By querying both `quiz` and
    # `question` we are making sure only the owner of the quiz can
    # change its details and also only questions that belongs to this
    # specific quiz can be changed via this url (in cases where the
    # user might have forged/player with the url params.
    exams = get_object_or_404(Exams, pk=exams_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, exams=exams)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )



    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('exams:update_exams', exams.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, 'classroom/teachers/exams_question_change_form.html', {
        'exams': exams,
        'question': question,
        'form': form,
        'formset': formset
    })


@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionDeleteView(BSModalDeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'classroom/teachers/exams_question_delete_confirm.html'
    pk_url_kwarg = 'question_pk'
    success_message = 'Success: Question was successully deleted'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['exams'] = question.exams
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'The question %s was deleted with success!' % question.text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(exams__owner=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('exams:update_exams', kwargs={'pk': question.exams_id})



class TakenExamsResultsView(DetailView):
    model = Answer
    template_name = 'classroom/students/exams_results.html'
    context_object_name = 'results'


class CreateExamForm(BSModalCreateView):
    template_name = 'classroom/teachers/create_exam.html'
    form_class = CreateExamForm
    success_message = 'Success: Exam successully created'
    success_url = reverse_lazy('exams:update_exams')


class ExamDelete(BSModalDeleteView):
    template_name = 'classroom/teachers/exams_delete.html'
    model = Exams
    success_message = 'Success: Exams was Deleted'
    success_url = reverse_lazy('exams:created_exams_list')


class ResultsView(BSModalReadView):
    model = Exams
    template_name = 'classroom/teachers/results.html'
    context_object_name = 'exams'


    def get_context_data(self, **kwargs):
        exams = self.get_object()
        taken_exams = exams.taken_exams.select_related('student__user').order_by('-score')
        total_taken_exams = taken_exams.count()
        exams_score = exams.taken_exams.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_exams': taken_exams,
            'total_taken_exams': total_taken_exams,
            'exams_score': exams_score
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.exams.all()



class CreateYearLevel(BSModalCreateView):
    template_name = 'classroom/teachers/yearlevel.html'
    form_class = Year_LevelForm
    success_message = 'Success: Year Level successully created'
    success_url = reverse_lazy('exams:create-new-exams')
