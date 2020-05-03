from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'handouts'
urlpatterns = [
    path('handouts/', views.ListofHandouts.as_view(), name='list-of-handouts'),
    path('handouts/upload-new-handouts/', views.UploadHandouts.as_view(), name='upload-handouts'),
    path('handouts-document/<int:pk>/delete/', views.FileDeleteView.as_view(), name='file_delete'),
    path('handouts/homepage-view/', views.HandoutsHomepageView.as_view(), name='handouts_homepage'),
    path('handouts/edu-video-list', views.ListofVideos.as_view(), name='list-of-videos'),
    path('handouts/video/upload-video/', views.VideoUpload.as_view(), name='uplaod-video'),

    path('handouts/video/list-of-uploaded-videos', views.ListofUploadedVideo.as_view(), name='list-of-uploaded-videos'),
    path('handouts/uploaded-video/<int:pk>/delete/', views.VideoDelete.as_view(), name='delete-video'),
    path('handouts/video/upload-video/', views.VideoUpload.as_view(), name='upload-video'),
    path('handouts/documents/list-of-uploaded-handouts/', views.ListofUploadedHandouts.as_view(), name = 'list-of-uploaded-handouts'),
    path('handouts/video/update-video/<int:pk>/' , views.VideoUpdate.as_view(), name = 'update-video'),
    path('handouts/uploaded-handouts/delete/<int:pk>/', views.HandoutsDelete.as_view() , name = 'delete-handouts'),
    path('handouts/uploaded-handouts/update/<int:pk>/', views.HandoutsUpdate.as_view(), name = 'update-handouts'),
] 
if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)