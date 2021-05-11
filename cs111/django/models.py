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

class LabGrade(models.Model):
    student = models.ForeignKey(Role, on_delete=models.CASCADE,
                                related_name='lab_grades')
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    commit_id = models.CharField(max_length=40)
    late_days = models.IntegerField()
    grade = models.IntegerField()

    def __str__(self):
        return f'{self.student} - {self.lab} - Grade: {self.grade} - Late Days: {self.late_days}'

    class Meta:
        unique_together = ['student', 'lab']

class MidtermGrade(models.Model):
    student = models.OneToOneField(Role, on_delete=models.CASCADE,
                                   related_name='midterm_grade')
    grade = models.FloatField()

    def __str__(self):
        return f'{self.student} - Grade: {self.grade}'
