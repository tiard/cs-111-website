from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from cs111.django.models import Lab, LabGrade, Offering

import argparse
import csv

class Command(BaseCommand):
    help = 'Adds lab gradesfrom a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('r'))
        parser.add_argument('lab_number', type=int)

    def handle(self, *args, **options):
        reader = csv.reader(options['csv'])
        offering = Offering.objects.get(slug=settings.CS111_OFFERING)
        lab = Lab.objects.get(offering=offering, number=options['lab_number'])
        for row in reader:
            username = row[0]
            commit_id = row[1]
            try:
                grade = int(row[2])
            except ValueError:
                continue
            late_days = int(row[3])

            user = User.objects.get(username=username)
            student = user.role

            lab_grade, created = LabGrade.objects.get_or_create(
                student=student,
                lab=lab,
                defaults={
                    'commit_id': commit_id,
                    'late_days': late_days,
                    'grade': grade,
                },
            )
            if not created:
                lab_grade.commit_id = commit_id
                lab_grade.late_days = late_days
                lab_grade.grade = grade
                lab_grade.save()
