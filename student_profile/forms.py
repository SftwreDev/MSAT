from django import forms

from .models import StudentProfile
from bootstrap_modal_forms.forms import BSModalForm


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['user', 'profile_picture', 'bio', 'first_name','middle_name', 'last_name', 'birthday', 'age','gender' ,'address',
        'contact_no', 'email', 'mothers_name', 'fathers_name', 'student_id','academic_level','program','section' ]



class ProfileForm(BSModalForm):
	class Meta:
		model = StudentProfile
		fields = ['user', 'profile_picture', 'bio', 'first_name','middle_name', 'last_name', 'birthday', 'age','gender' ,'address',
        'contact_no', 'email', 'mothers_name', 'fathers_name', 'student_id','academic_level','program','section' ]
