from django.db import models

from django.contrib.auth.models import User
from django_gitolite.models import Repo

from .storages import OverwriteFileSystemStorage

class Offering(models.Model):
    slug = models.SlugField()

    def __str__(self):
        return self.slug

class File(models.Model):
    file = models.FileField(upload_to='cs111', storage=OverwriteFileSystemStorage)

    def __str__(self):
        return str(self.file)

class Lecture(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE,
                                 related_name='lectures')
    number = models.SmallIntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='cs111/lectures', storage=OverwriteFileSystemStorage)
    youtube = models.URLField(blank=True)
    youtube2 = models.URLField(blank=True)

    def __str__(self):
        return f'{self.title} (Lecture {self.number})'

class Lab(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE,
                                 related_name='labs')
    number = models.SmallIntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='cs111/labs', storage=OverwriteFileSystemStorage)
    due_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.title} (Lab {self.number})'

class Role(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE,
                                 related_name='roles')
    ucla_id = models.IntegerField(blank=True, null=True, unique=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='role',
    )
    INSTRUCTOR = 'I'
    TA = 'T'
    STUDENT = 'S'
    AUDIT = 'A'
    ROLE_CHOICES = [
        (INSTRUCTOR, 'Instructor'),
        (TA, 'TA'),
        (STUDENT, 'Student'),
        (AUDIT, 'Audit'),
    ]
    role = models.CharField(
        max_length=1, choices=ROLE_CHOICES)

    def __str__(self):
        display = self.get_role_display()
        return f'{self.user} ({display})'

class LabGrade(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE,
                                 related_name='lab_grades')
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
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE,
                                 related_name='midterm_grades')
    student = models.OneToOneField(Role, on_delete=models.CASCADE,
                                   related_name='midterm_grade')
    grade = models.FloatField()

    def __str__(self):
        return f'{self.student} - Grade: {self.grade}'

class FinalExamGrade(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE,
                                 related_name='final_exam_grades')
    student = models.OneToOneField(Role, on_delete=models.CASCADE,
                                   related_name='final_exam_grade')
    grade = models.FloatField()

    def __str__(self):
        return f'{self.student} - Grade: {self.grade}'

class EvaluationGrade(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE,
                                 related_name='evaluation_grades')
    student = models.OneToOneField(Role, on_delete=models.CASCADE,
                                   related_name='evaluation_grade')
    grade = models.FloatField()

    def __str__(self):
        return f'{self.student} - Grade: {self.grade}'

class CourseGrade(models.Model):
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE,
                                 related_name='course_grades')
    student = models.OneToOneField(Role, on_delete=models.CASCADE,
                                   related_name='course_grade')
    grade = models.FloatField()

    def __str__(self):
        return f'{self.student} - Grade: {self.grade}'

class UpstreamStatus(models.Model):
    repo = models.OneToOneField(Repo, on_delete=models.CASCADE,
                                related_name='upstream_status')
    is_merged = models.BooleanField()

    def __str__(self):
        return str(self.repo)

class SubmissionStatus(models.Model):
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE,
                             related_name='submission_statuses')
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE,
                            related_name='submission_statuses')
    is_modified = models.BooleanField()

    def __str__(self):
        return f'{self.repo} - {self.lab}'

    class Meta:
        unique_together = ['repo', 'lab']
