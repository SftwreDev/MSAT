from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic import ListView

from django.urls import reverse_lazy

from .models import Handouts, Videos
from .forms import HandoutsForm, VideoForm
from .filters import HandoutsSearch, VideoSearch
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from quiz.decorators import student_required, teacher_required
from bootstrap_modal_forms.generic import (BSModalLoginView,
                                           BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)

class ListofHandouts(ListView):
    model = Handouts
    template_name = 'handouts/list_of_handouts.html'
    context_object_name = 'list_of_handouts'
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = HandoutsSearch(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        student = self.request.user.student
        student_year_level = student.year_level.values_list('pk', flat=True)
        queryset = Handouts.objects.filter(year_level__in=student_year_level)
        return queryset

class ListofUploadedHandouts(ListView):
    model = Handouts
    template_name = 'handouts/list_of_uploaded_handouts.html'
    context_object_name = 'handouts'
    ordering = ['name']


class UploadHandouts(BSModalCreateView):
    template_name = 'handouts/upload_handouts.html'
    form_class = HandoutsForm
    succes_message = 'Success: Handouts successfully uploaded'
    success_url = reverse_lazy("handouts:list-of-uploaded-handouts")

@method_decorator([login_required, teacher_required], name='dispatch')
class FileDeleteView(DeleteView):
    model = Handouts
    context_object_name = 'file'
    template_name = 'handouts/confirm_delete.html'
    success_url = reverse_lazy('handouts:list-of-handouts')

class HandoutsHomepageView(TemplateView):
    template_name = 'handouts/handouts_homepage.html'


""" Video Category Part"""
@method_decorator([login_required, teacher_required], name='dispatch')
class VideoUpload(BSModalCreateView):
    template_name = 'handouts/upload_video.html'
    form_class = VideoForm
    success_message = "Success: Video uploaded successfully"
    success_url = reverse_lazy('handouts:list-of-uploaded-videos')

class VideoDelete(BSModalDeleteView):
    model = Videos
    template_name = 'handouts/delete_video.html'
    success_message = 'Success: Video successfully deleted'
    success_url = reverse_lazy('handouts:list-of-uploaded-videos')

class ListofUploadedVideo(ListView):
    model = Videos
    template_name = 'handouts/list_of_uploaded_videos.html'
    context_object_name = 'videos'
    ordering = ['title']


class ListofVideos(ListView):
    model = Videos
    template_name = 'handouts/list_of_videos.html'
    context_object_name = 'list_of_videos'
    ordering = ['title']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = VideoSearch(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        student = self.request.user.student
        student_year_level = student.year_level.values_list('pk', flat=True)
        queryset = Videos.objects.filter(year_level__in=student_year_level)
        return queryset


class VideoUpdate(BSModalUpdateView):
    model = Videos
    template_name = 'handouts/update_video.html'
    form_class = VideoForm
    success_message = 'Success : Video updated successfully'
    success_url = reverse_lazy("handouts:list-of-uploaded-videos")


class HandoutsDelete(BSModalDeleteView):
    model = Handouts
    template_name  = 'handouts/delete_handouts.html'
    success_message = 'Success : Handouts updated successfully'
    success_url = reverse_lazy('handouts:list-of-uploaded-handouts')

class HandoutsUpdate(BSModalUpdateView):
    model = Handouts
    template_name = 'handouts/update_handouts.html'
    form_class = HandoutsForm
    success_message = 'Success : Handouts updated successfully'
    success_url = reverse_lazy("handouts:list-of-uploaded-handouts")
