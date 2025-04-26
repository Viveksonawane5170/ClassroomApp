# student/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import StudentSignUpForm, StudentSignInForm

def index(request):
    return render(request, 'student/index.html')

def signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='student.backends.StudentBackend')
            messages.success(request, 'Registration successful.')
            return redirect('student:index')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = StudentSignUpForm()
    return render(request, 'student/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = StudentSignInForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password, backend='student.backends.StudentBackend')
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('student:index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = StudentSignInForm()
    return render(request, 'student/signin.html', {'form': form})

def signout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect('student:index')