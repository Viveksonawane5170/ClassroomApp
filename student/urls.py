from django.urls import path
from . import views

app_name = 'student'  # Make sure this line exists

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("video/<int:video_id>/", views.view_video, name="view_video"),
]