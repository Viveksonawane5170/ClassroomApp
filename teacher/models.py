# teacher/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Teacher(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=100, blank=True)
    
    # Add these to fix the reverse accessor clash
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this teacher belongs to.',
        related_name="teacher_groups",
        related_query_name="teacher",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this teacher.',
        related_name="teacher_user_permissions",
        related_query_name="teacher",
    )
    
    def __str__(self):
        return self.username
    
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title