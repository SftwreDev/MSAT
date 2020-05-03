from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe

from quiz.models import User, Student, Year_Level, Exams




class Question(models.Model):
    exams = models.ForeignKey(Exams, on_delete=models.CASCADE,related_name='questions', help_text="Exams")
    text = models.CharField('Question', max_length=255,help_text='Insert your question here')
    

    def __str__(self):
        return self.text


class Answer(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', help_text='Question')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)


    def __str__(self):
        return self.text



class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exams_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


