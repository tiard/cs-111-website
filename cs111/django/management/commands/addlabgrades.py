from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from cs111.django.models import Lab, LabGrade

import argparse
import csv

class Command(BaseCommand):
    help = 'Adds lab gradesfrom a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('r'))
        parser.add_argument('lab')

    def handle(self, *args, **options):
        reader = csv.reader(options['csv'])
        lab = Lab.objects.get(number=options['lab'])
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

            try:
                LabGrade.objects.create(
                    student=student,
                    lab=lab,
                    commit_id=commit_id,
                    late_days=late_days,
                    grade=grade,
                )
            except Exception as e:
                print(e)
