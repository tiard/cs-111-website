from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Offering, File, Lecture, Lab, LabGrade, MidtermGrade, FinalExamGrade, EvaluationGrade, CourseGrade
from django_gitolite.models import Repo

class LecturesView(generic.ListView):
    template_name = 'cs111/lectures.html'
    context_object_name = 'lectures'

    def get_queryset(self):
        offering = Offering.objects.get(slug=settings.CS111_OFFERING)
        return Lecture.objects.filter(offering=offering).order_by('number')

class LabsView(generic.ListView):
    template_name = 'cs111/labs.html'
    context_object_name = 'labs'

    def get_queryset(self):
        offering = Offering.objects.get(slug=settings.CS111_OFFERING)
        return Lab.objects.filter(offering=offering).order_by('number')

def index(request):
    return render(request, 'cs111/index.html', {})

def labs(request):
    return render(request, 'cs111/labs.html', {})

@login_required
def grades(request):
    user = request.user
    offering_slug = settings.CS111_OFFERING
    try:
        repo = Repo.objects.get(path=f'{offering_slug}/{user.username}/cs111')
    except Repo.DoesNotExist:
        repo = None
    lab_grades = LabGrade.objects.filter(student__user=user).order_by('lab__number')
    midterm_grade = None
    try:
        midterm_grade = MidtermGrade.objects.get(student__user=user)
    except Exception as e:
        pass

    final_exam_grade = None
    try:
        final_exam_grade = FinalExamGrade.objects.get(student__user=user)
    except Exception as e:
        pass

    evaluation_grade = None
    try:
        evaluation_grade = EvaluationGrade.objects.get(student__user=user)
    except Exception as e:
        pass

    course_grade = None
    try:
        course_grade = CourseGrade.objects.get(student__user=user)
    except Exception as e:
        pass
    return render(request, 'cs111/grades.html', {
        'repo': repo,
        'evaluation_grade': evaluation_grade,
        'lab_grades': lab_grades,
        'midterm_grade': midterm_grade,
        'final_exam_grade': final_exam_grade,
        'course_grade': course_grade,
    })

def resources(request):
    try:
        syllabus = File.objects.get(file='cs111/syllabus.pdf')
    except File.DoesNotExist:
        syllabus = None
    try:
        vm = File.objects.get(file='cs111/vm.ova')
    except File.DoesNotExist:
        vm = None
    try:
        vm_no_gui = File.objects.get(file='cs111/vm-no-gui.ova')
    except File.DoesNotExist:
        vm_no_gui = None
    try:
        summer21_midterm = File.objects.get(file='cs111/summer21-midterm.pdf')
    except File.DoesNotExist:
        summer21_midterm = None
    try:
        summer21_midterm_solutions = File.objects.get(file='cs111/summer21-midterm-solutions.pdf')
    except File.DoesNotExist:
        summer21_midterm_solutions = None
    try:
        fall21_midterm = File.objects.get(file='cs111/fall21-midterm.pdf')
    except File.DoesNotExist:
        fall21_midterm = None
    try:
        fall21_midterm_solutions = File.objects.get(file='cs111/fall21-midterm-solutions.pdf')
    except File.DoesNotExist:
        fall21_midterm_solutions = None

    return render(request, 'cs111/resources.html', {
        'syllabus': syllabus,
        'vm': vm,
        'vm_no_gui': vm_no_gui,
        'summer21_midterm': summer21_midterm,
        'summer21_midterm_solutions': summer21_midterm_solutions,
    })
