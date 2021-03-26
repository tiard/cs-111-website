from django.core.management.base import BaseCommand, CommandError

from cs111.django.models import Role

from ._private import add_user

class Command(BaseCommand):
    help = 'Add a TA from the command line'

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('email')
        parser.add_argument('first_name')
        parser.add_argument('last_name')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        first_name = options['first_name']
        last_name = options['last_name']

        add_user(username, email, first_name, last_name, Role.TA)
