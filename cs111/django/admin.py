from django.contrib import admin

from .models import *

admin.site.register(Offering)
admin.site.register(File)
admin.site.register(Lecture)
admin.site.register(Lab)
admin.site.register(Role)
admin.site.register(LabGrade)
admin.site.register(MidtermGrade)
admin.site.register(FinalExamGrade)
admin.site.register(EvaluationGrade)
admin.site.register(CourseGrade)
admin.site.register(UpstreamStatus)
admin.site.register(SubmissionStatus)
