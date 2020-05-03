import django_filters


from .models import Handouts, Videos

class HandoutsSearch(django_filters.FilterSet):
    
    class Meta:
        model = Handouts
        fields = {'category' : ['icontains']}



class VideoSearch(django_filters.FilterSet):
    
    class Meta:
        model = Videos
        fields = {'category' : ['icontains']}