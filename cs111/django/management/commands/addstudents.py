from django.core.management.base import BaseCommand, CommandError

from cs111.django.models import Role

from ._private import add_user

import argparse
import csv

class Command(BaseCommand):
    help = 'Adds students from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('r'))

    def _first_name(self, s):
        return s.strip().title()

    def _last_name(self, s):
        return s.strip().title().replace('De ', 'de ')

    def handle(self, *args, **options):
        reader = csv.reader(options['csv'])
        is_body = False
        usernames = set()
        for row in reader:
            if 'Name' in row:
                is_body = True
                continue
            if not is_body:
                continue
            if len(row) == 0:
                continue
            name = row[1]
            email = row[2].lower()
            s = name.split(',')
            assert len(s) in [2, 3]
            first_name = self._first_name(s[1])
            if len(s) == 2:
                last_name = self._last_name(s[0])
            elif len(s) == 3:
                last_name = self._last_name(f'{s[0]}{s[2]}')

            s = first_name.split()
            user_first = ''.join(x[0] for x in s).lower()
            s = last_name.split()
            if len(s) > 3:
                user_second = ''.join(x[0] for x in s).lower()
            else:
                user_second = ''.join(x.lower() for x in s)
            username = f'{user_first}{user_second}'

            assert username not in usernames
            usernames.add(username)

            add_user(username, email, first_name, last_name, Role.STUDENT)

            self.stdout.write(self.style.SUCCESS(f'Added student "{username}"'))
