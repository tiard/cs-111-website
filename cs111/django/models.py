from django.db import models

from django.contrib.auth.models import User

from .storages import OverwriteFileSystemStorage

class File(models.Model):
    file = models.FileField(upload_to='cs111', storage=OverwriteFileSystemStorage)

    def __str__(self):
        return str(self.file)

class Lecture(models.Model):
    number = models.SmallIntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='cs111/lectures', storage=OverwriteFileSystemStorage)
    youtube = models.URLField(blank=True)
    youtube2 = models.URLField(blank=True)

    def __str__(self):
        return f'{self.title} (Lecture {self.number})'

class Lab(models.Model):
    number = models.SmallIntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='cs111/labs', storage=OverwriteFileSystemStorage)

    def __str__(self):
        return f'{self.title} (Lab {self.number})'

class Role(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='role',
    )
    INSTRUCTOR = 'I'
    TA = 'T'
    STUDENT = 'S'
    ROLE_CHOICES = [
        (INSTRUCTOR, 'Instructor'),
        (TA, 'TA'),
        (STUDENT, 'Student'),
    ]
    role = models.CharField(
        max_length=1, choices=ROLE_CHOICES)

    def __str__(self):
        display = self.get_role_display()
        return f'{self.user} ({display})'
