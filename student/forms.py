# student/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Student

class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Student
        fields = ('username', 'email', 'password1', 'password2', 
                 'first_name', 'last_name', 'student_id', 'grade_level', 'parent_phone')

class StudentSignInForm(AuthenticationForm):
    class Meta:
        model = Student
        fields = ('username', 'password')