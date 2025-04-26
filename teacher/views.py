from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the teacher index.")


# teacher/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import TeacherSignUpForm, TeacherSignInForm

def index(request):
    return render(request, 'teacher/index.html')

def signup(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('index')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = TeacherSignUpForm()
    return render(request, 'teacher/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = TeacherSignInForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = TeacherSignInForm()
    return render(request, 'teacher/signin.html', {'form': form})

def signout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect('index')