# student/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Student(AbstractUser):
    student_id = models.CharField(max_length=20, unique=True)
    grade_level = models.IntegerField()
    parent_phone = models.CharField(max_length=15, blank=True)
    
    # Add these to fix the reverse accessor clash
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this student belongs to.',
        related_name="student_groups",
        related_query_name="student",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this student.',
        related_name="student_user_permissions",
        related_query_name="student",
    )
    
    def __str__(self):
        return self.username