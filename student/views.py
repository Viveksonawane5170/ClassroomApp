# student/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import StudentSignUpForm, StudentSignInForm

# student/views.py
from teacher.models import Video

def index(request):
    videos = Video.objects.all() if request.user.is_authenticated else None
    return render(request, 'student/index.html', {'videos': videos})

def view_video(request, video_id):
    video = Video.objects.get(id=video_id)
    return render(request, 'student/view_video.html', {'video': video})

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


# Add at the top
from teacher.models import Video
from django.http import JsonResponse
from dgvideo import transcribe_with_deepgram, extract_audio
import tempfile
import os

def get_transcript(request, video_id):
    if request.method == 'POST':
        try:
            video = Video.objects.get(id=video_id)
            
            # Create temp file for audio extraction
            with tempfile.NamedTemporaryFile(delete=False) as temp_video:
                for chunk in video.video_file.chunks():
                    temp_video.write(chunk)
                temp_video_path = temp_video.name

            # Extract audio
            audio_file = extract_audio(temp_video_path)
            
            # Transcribe
            transcript = transcribe_with_deepgram(audio_file)
            
            # Cleanup
            os.unlink(temp_video_path)
            if audio_file and os.path.exists(audio_file):
                os.unlink(audio_file)

            return JsonResponse({'transcript': transcript})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


# Add at the top
from lamma import generate_summary

def get_summary(request, video_id):
    if request.method == 'POST':
        transcript = request.POST.get('transcript', '')
        if transcript:
            summary = generate_summary(transcript)
            return JsonResponse({'summary': summary})
        return JsonResponse({'error': 'No transcript provided'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


# student/views.py (add this at the bottom)
from lamma import generate_questions

def get_questions(request, video_id):
    if request.method == 'POST':
        summary = request.POST.get('summary', '')
        if summary:
            questions = generate_questions(summary)
            return JsonResponse({'questions': questions})
        return JsonResponse({'error': 'No summary provided'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)