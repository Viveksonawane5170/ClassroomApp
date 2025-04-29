# student/urls.py
from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("video/<int:video_id>/", views.view_video, name="view_video"),
    path('video/<int:video_id>/transcript/', views.get_transcript, name='get_transcript'),
    path('video/<int:video_id>/summary/', views.get_summary, name='get_summary'),
    path('video/<int:video_id>/questions/', views.get_questions, name='get_questions'),  # New line
]