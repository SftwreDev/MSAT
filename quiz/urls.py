from django.urls import include, path

from quiz import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),

    
    
    path('students/', views.StudentsQuizListView.as_view(), name='quiz_list'),
    path('students/', include(([
        path('interests/', views.StudentInterestsView.as_view(), name='student_interests'),
        path('taken/', views.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', views.take_quiz, name='take_quiz'),
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', views.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', views.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', views.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', views.QuizDelete.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', views.ResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', views.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', views.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
        path('year_level/', views.Create_YearLevel.as_view(), name='year_level' ),
    ], 'classroom'), namespace='teachers')),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', views.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/teacher/', views.TeacherSignUpView.as_view(), name='teacher_signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


