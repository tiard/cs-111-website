from django.core.management.base import BaseCommand, CommandError

from cs111.django.models import Role
from django_gitolite.models import Repo
from django_gitolite.utils import home_dir

import argparse
import csv
import datetime
import os
import pygit2
import pytz

class Command(BaseCommand):
    help = 'Gets commits from right now'
    tz = pytz.timezone("America/Los_Angeles")
    due_dates = {
      'lab-02':
         datetime.datetime(2021, 5, 10, 20, tzinfo=tz).astimezone(pytz.utc),
    }

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('w'))
        parser.add_argument('lab', type=str)

    def handle(self, *args, **options):
        writer = csv.writer(options['csv'])
        lab = options['lab']
        for role in Role.objects.filter(role=Role.STUDENT).order_by('user__username'):
            user = role.user
            username = user.username
            path = f'spring21/{username}/cs111'
            repo = Repo.objects.get(path=path)
            pushes = repo.pushes.filter(refname='refs/heads/main').order_by('-time')

            git_repo = pygit2.Repository(
                os.path.join(home_dir(), 'repositories', '{}.git'.format(path))
            )
            found = False
            for push in pushes:
                late_days = (push.time - self.due_dates['lab-02']).days + 1
                late_days = late_days if late_days > 0 else 0
                for patch in git_repo.diff(push.old_rev, push.new_rev):
                    delta = patch.delta
                    if delta.status == pygit2.GIT_DELTA_ADDED or delta.status == pygit2.GIT_DELTA_MODIFIED:
                        if delta.new_file.path.startswith(lab):
                            found = True
                            break
                if found:
                    writer.writerow([username, push.new_rev, late_days])
                    break

            if not found:
                writer.writerow([username, '0000000000000000000000000000000000000000', 0])
