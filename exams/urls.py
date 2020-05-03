from django.urls import include, path

from exams import views

app_name = 'exams'
urlpatterns = [
    
    path('students/', views.StudentsExamsListView.as_view(), name='exams_list'),
    path('students/exams/<int:pk>/', views.take_exams, name='take_exams_form'),
    path('students/taken/', views.TakenExamsListView.as_view(), name='taken_exams_list'),
    path('students/taken-exams/results/<int:pk>/', views.TakenExamsResultsView.as_view(), name='taken_exams_results'),
    path('teachers/create-exams/', views.ExamsCreateView.as_view(), name='create-new-exams'),
    path('teachers/list-of-exams/', views.TeachersExamsListView.as_view(), name='created_exams_list'),
    path('teachers/update-exams/<int:pk>/', views.ExamsUpdateView.as_view(), name = 'update_exams'),
    path('teachers/<int:pk>/delete-exams/', views.ExamDelete.as_view(), name='exams_delete'),
    path('teachers/exams/<int:pk>/question/add/', views.exams_question_add, name='exams_question_add'),
    path('teachers/exams/<int:exams_pk>/question/<int:question_pk>/', views.question_change, name='exams_question_change'),
    #path('teachers/exams/<int:exams_pk>/question/<int:question_pk>/', views.question_change, name='question_change'),
    path('teachers/exams/<int:pk>/results/', views.ResultsView.as_view(), name='exams_results'),
    path('teachers/exams/<int:exams_pk>/question/<int:question_pk>/delete/', views.QuestionDeleteView.as_view(), name='exams_question_delete'),

    path('teachers/create-year-level/', views.CreateYearLevel.as_view(), name='add_year_level'),
]

