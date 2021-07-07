from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from cs111.django.models import Offering, Role, Lab
from django_gitolite.models import Repo
from django_gitolite.utils import home_dir

import argparse
import csv
import datetime
import os
import pygit2

class Command(BaseCommand):
    help = 'Gets commits from right now'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('w'))
        parser.add_argument('lab_number', type=int)

    def handle(self, *args, **options):
        writer = csv.writer(options['csv'])

        offering = Offering.objects.get(slug=settings.CS111_OFFERING)
        lab = Lab.objects.get(offering=offering, number=options['lab_number'])

        for role in Role.objects.filter(role=Role.STUDENT, offering=offering).order_by('user__username'):
            user = role.user
            username = user.username
            path = f'{offering.slug}/{username}/cs111'
            repo = Repo.objects.get(path=path)
            pushes = repo.pushes.filter(refname='refs/heads/main').order_by('-time')

            git_repo = pygit2.Repository(
                os.path.join(home_dir(), 'repositories', '{}.git'.format(path))
            )
            found = False
            for push in pushes:
                late_days = (push.time - lab.due_date).days + 1
                late_days = late_days if late_days > 0 else 0
                for patch in git_repo.diff(push.old_rev, push.new_rev):
                    delta = patch.delta
                    if delta.status == pygit2.GIT_DELTA_ADDED or delta.status == pygit2.GIT_DELTA_MODIFIED:
                        if delta.new_file.path.startswith(f'lab-{lab.number:02}'):
                            found = True
                            break
                if found:
                    writer.writerow([username, push.new_rev, late_days])
                    break

            if not found:
                writer.writerow([username, '0000000000000000000000000000000000000000', 0])
