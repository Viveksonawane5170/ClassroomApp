from django.shortcuts import render, redirect
from .forms import VideoUploadForm
from .models import Video
from django.contrib import messages

# Create your views here.
def index(request):
    videos = Video.objects.filter(teacher=request.user) if request.user.is_authenticated else None
    return render(request, 'teacher/index.html', {'videos': videos})


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
            return redirect('teacher:index')
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
                return redirect('teacher:index')
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
    return redirect('teacher:index')


def upload_video(request):
    if not request.user.is_authenticated:
        return redirect('teacher:signin')
        
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.teacher = request.user
            video.save()
            messages.success(request, 'Video uploaded successfully!')
            return redirect('teacher:index')
    else:
        form = VideoUploadForm()
    return render(request, 'teacher/upload_video.html', {'form': form})

# teacher/views.py
from student.models import Student  # Add this import at the top

# Add this new view function
# teacher/views.py

def student_list(request):
    if not request.user.is_authenticated:
        return redirect('teacher:signin')
    
    students = Student.objects.all()
    return render(request, 'teacher/student_list.html', {'students': students})

def index(request):
    if not request.user.is_authenticated:
        return redirect('teacher:signin')
    
    videos = Video.objects.filter(teacher=request.user)
    students_count = Student.objects.count()  # Add this line
    return render(request, 'teacher/index.html', {
        'videos': videos,
        'students_count': students_count  # Add this line
    })

