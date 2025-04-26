# teacher/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Teacher

class TeacherSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Teacher
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'subject')

class TeacherSignInForm(AuthenticationForm):
    class Meta:
        model = Teacher
        fields = ('username', 'password')

# teacher/forms.py
from django import forms
from .models import Video

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail']