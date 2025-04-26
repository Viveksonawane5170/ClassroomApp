# teacher/backends.py
from django.contrib.auth.backends import ModelBackend
from .models import Teacher

class TeacherBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Teacher.objects.get(username=username)
            if user.check_password(password):
                return user
        except Teacher.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Teacher.objects.get(pk=user_id)
        except Teacher.DoesNotExist:
            return None