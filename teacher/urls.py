from django.urls import path
from . import views

app_name = 'teacher'  # This is crucial for namespacing

urlpatterns = [
    path("", views.index, name="index"),  # This defines the 'index' URL name
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
]