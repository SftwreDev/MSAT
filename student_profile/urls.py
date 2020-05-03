from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'profile'

urlpatterns = [
    path('profile/student-profile-list/', views.StudentProfileView.as_view(), name='student-profile'),
    path('profile/create-student-profile/', views.ProfileCreate.as_view(), name='student-create-profile'),
    path('profile/about-student-profile/', views.StudentAboutProfileView.as_view(), name='student-profile-about'),
    path('profile/student-taken-quiz-profile/', views.TakenQuizListProfileView.as_view(), name='student-taken-quiz'),
    path('profile/student-taken-exams-profile/', views.TakenExamsListProfileView.as_view(), name='student-taken-exams'),
    path('profile/student-options-profile/', views.StudentOptionProfileView.as_view(), name='student-options-profile'),
    path('profile/student-update-profile/<int:pk>/', views.ProfileUpdate.as_view(), name='student-update-profile'),
    path('profile/student-profile/<int:pk>/delete/', views.ProfileDelete.as_view(), name='student_profile_delete'),

    path('profile/list-of-student-profile/', views.ListOfStudentView.as_view(), name='list-of-student'),
    path('profile/list-of-year-level/<int:pk>/', views.YearLevelDelete.as_view(), name='yearlevel-delete'),
    path('profile/create-new-year-level' , views.Create_YearLevel.as_view(), name='yearlevel-add'),
]


if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
