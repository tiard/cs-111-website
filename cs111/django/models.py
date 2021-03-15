from django.db import models

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

    def __str__(self):
        return f'{self.title} (Lecture {self.number})'
