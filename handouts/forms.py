from django import forms

from .models import Handouts, Videos
from bootstrap_modal_forms.forms import BSModalForm

class HandoutsForm(BSModalForm):
    class Meta:
        model = Handouts
        fields = ['name', 'year_level', 'description', 'category','documents']


class VideoForm(BSModalForm):
    class Meta:
        model = Videos
        fields = ['title','year_level', 'description','category','video']
