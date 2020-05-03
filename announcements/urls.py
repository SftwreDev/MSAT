from django.urls import path

from . import views

app_name = 'announcements'
urlpatterns = [
    path('announcements/', views.AnnouncementsList.as_view(), name='list-of-announcements'),
    path('announcementts/list-of-created-announcements/', views.PostedAnnouncementsList.as_view(), name='create-announcements'),
    path('announcements/post-announcements/', views.CreateAnnouncements.as_view(), name='post-announcements'),
    path('announcements/view-posted-announcements/<int:pk>', views.AnnouncementsView.as_view(), name='view-posted-announcements'),
    path('announcements/announcements-delete/<int:pk>', views.AnnouncementsDelete.as_view(), name='post-delete'),
    path('announcements/announcement-update/<int:pk>' , views.AnnouncementsUpdate.as_view(), name='post-edit'),
]
