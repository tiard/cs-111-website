from django.contrib import admin

from .models import File, Lecture, Lab, Role, LabGrade, MidtermGrade, FinalExamGrade

admin.site.register(File)
admin.site.register(Lecture)
admin.site.register(Lab)
admin.site.register(Role)
admin.site.register(LabGrade)
admin.site.register(MidtermGrade)
admin.site.register(FinalExamGrade)
