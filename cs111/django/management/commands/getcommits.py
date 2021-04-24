from django.core.management.base import BaseCommand, CommandError

from cs111.django.models import Role
from django_gitolite.models import Repo

import argparse
import csv

class Command(BaseCommand):
    help = 'Gets commits from right now'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('w'))

    def handle(self, *args, **options):
        writer = csv.writer(options['csv'])
        for role in Role.objects.filter(role=Role.STUDENT):
            user = role.user
            username = user.username
            path = f'spring21/{username}/cs111'
            repo = Repo.objects.get(path=path)
            pushes = repo.pushes.filter(refname='refs/heads/main').order_by('-time')
            if pushes.count() > 0:
                rev = pushes[0].new_rev
            else:
                rev = '0000000000000000000000000000000000000000'
            writer.writerow([username, rev])
