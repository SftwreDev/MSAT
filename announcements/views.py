from django.shortcuts import render, redirect


from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from quiz.decorators import student_required, teacher_required
from .models import Announcements
from .forms import CreateAnnouncementsForm
from django.urls import reverse, reverse_lazy
from bootstrap_modal_forms.generic import (BSModalLoginView,
                                           BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)

@method_decorator([login_required, student_required], name='dispatch')
class AnnouncementsList(ListView):
    model = Announcements
    template_name = 'announcements/announcements_board.html'
    context_object_name = 'announcements'

    def get_queryset(self):
        student = self.request.user.student
        student_year_level = student.year_level.values_list('pk', flat=True)
        queryset = Announcements.objects.filter(year_level__in=student_year_level)
        return queryset

class PostedAnnouncementsList(ListView):
    model = Announcements
    template_name = 'announcements/create_announcement.html'
    context_object_name = 'announcements'
    ordering = ['date', ]

@method_decorator([login_required, teacher_required], name='dispatch')
class CreateAnnouncements(BSModalCreateView):
    template_name = 'announcements/post-announcement.html'
    form_class = CreateAnnouncementsForm
    success_message = 'Success: Announcements successully created'
    success_url = reverse_lazy('announcements:create-announcements')



class AnnouncementsView(BSModalReadView):
    model = Announcements
    template_name = 'announcements/view-announcements.html'
    context_object_name = 'announcements'


class AnnouncementsDelete(BSModalDeleteView):
    template_name = 'announcements/deletepost.html'
    model = Announcements
    success_message = 'Success: Announcements was Deleted'
    success_url = reverse_lazy('announcements:create-announcements')


class AnnouncementsUpdate(BSModalUpdateView):
    model = Announcements
    template_name = 'announcements/postupdate.html'
    form_class = CreateAnnouncementsForm
    success_message = 'Success : Announcements updated successfully'
    success_url = reverse_lazy("announcements:create-announcements")
