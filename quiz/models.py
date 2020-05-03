from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe

from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Year_Level(models.Model):
    name = models.CharField(max_length=30, help_text='Year Level')

    def __str__(self):
        return self.name

class Exams(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams')
    name = models.CharField(max_length=255, help_text='Exams Title')
    year_level = models.ForeignKey(Year_Level, on_delete = models.CASCADE,related_name='exams', help_text='Year_Level')

    def __str__(self):
        return self.name

class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255, help_text='Quiz Title')
    year_level = models.ForeignKey(Year_Level, on_delete = models.CASCADE,related_name='quizzes', help_text='Year Level')

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', help_text="Quiz")
    text = models.CharField('Question', max_length=255,help_text='Insert your question here')

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', help_text='Question')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)


    def __str__(self):
        return self.text


class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    examinations = models.ManyToManyField(Exams, through='TakenExams')
    year_level = models.ManyToManyField(Year_Level,related_name='year_level', blank=True)




    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions


    def get_unanswered_exams(self, exams):
        answered_questions = self.exams_answers \
            .filter(answer__question__exams=exams) \
            .values_list('answer__question__pk', flat=True)
        questions = exams.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username



class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

class TakenExams(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_exams')
    exams = models.ForeignKey(Exams, on_delete=models.CASCADE, related_name='taken_exams')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
