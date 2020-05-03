from django import forms

from .models import Announcements


from bootstrap_modal_forms.forms import BSModalForm


class CreateAnnouncementsForm(BSModalForm):
    class Meta:
        model = Announcements
        fields = ['title','year_level', 'content']
