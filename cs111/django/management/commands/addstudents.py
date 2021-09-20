from django.core.management.base import BaseCommand, CommandError

from cs111.django.models import Role

from ._private import add_user, update_user

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

        # Get all the existing usernames
        usernames = set()
        for role in Role.objects.all():
            usernames.add(role.user.username)

        is_body = False
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

            ucla_id = int(row[0].replace('-', ''))

            # Check for any repeat students
            if username in usernames:
               try:
                   updated = update_user(username, ucla_id)
               except:
                   self.stdout.write(self.style.ERROR(f'Failed to update student "{username}"'))
                   raise

               if updated:
                   continue
               else:
                   assert not Role.objects.filter(ucla_id=ucla_id).exists()
                   self.stdout.write(self.style.NOTICE(f'Conflict with student "{username}" ({ulca_id})'))

            assert username not in usernames
            usernames.add(username)

            try:
                add_user(username, email, first_name, last_name, Role.STUDENT, ucla_id=ucla_id)
            except:
                self.stdout.write(self.style.ERROR(f'Failed to add student "{username}"'))
                raise
