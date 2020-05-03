import django_filters


from .models import StudentProfile

class StudentSearch(django_filters.FilterSet):
    class Meta:
        model = StudentProfile
        fields = {'section' : ['exact']}
