from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth.models import User
from cs111.django.models import Role, Offering

def add_user(username, email, first_name, last_name, role, ucla_id=None):
    try:
        User.objects.get(username=username)
        return False
    except User.DoesNotExist:
        pass
    password = User.objects.make_random_password(length=16)
    user = User.objects.create_user(
        username,
        email,
        password,
        first_name=first_name,
        last_name=last_name
    )

    offering = Offering.objects.get(slug=settings.CS111_OFFERING)
    Role.objects.create(user=user, role=role,
                        offering=offering, ucla_id=ucla_id)

    send_mail(
        '[cs111] Welcome to Operating System Principles!',
        f'''Hi {first_name},

Please find your login information for https://laforge.cs.ucla.edu/cs111/ below.

    Username: {username}
    Password: {password}

I'm looking forward to this quarter!

Jon''',
        None,
        [email],
        fail_silently=False,
    )
    return True
