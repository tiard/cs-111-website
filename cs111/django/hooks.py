import csv
import logging
import os
import subprocess

from django.conf import settings
from django.contrib.auth.models import User

from django_gitolite.models import Repo
from django_gitolite.utils import home_dir

from cs111.django.models import Lab, LabGrade, Offering, Role, SubmissionStatus, UpstreamStatus

logger = logging.getLogger(__name__)

def update_grades(push):
    offering_slug = settings.CS111_OFFERING
    offering = Offering.objects.get(slug=offering_slug)

    repo = push.repo
    repo_path = repo.path

    git_path = os.path.join(home_dir(), 'repositories', f'{repo_path}.git')

    sudo_cmd = ['sudo', '-n', '-u', settings.GITOLITE_USER]

    for n in range(5):
        try:
            lab = Lab.objects.get(offering=offering, number=n)
        except Lab.DoesNotExist:
            continue

        result = subprocess.run(sudo_cmd + ['git', 'show', f'{push.new_rev}:lab{n}-grades.csv'], cwd=git_path, capture_output=True, text=True)
        if result.returncode != 0:
            continue
        reader = csv.reader(result.stdout.splitlines())
        for row in reader:
            username = row[0]
            commit_id = row[1]
            late_days = row[2]
            grade = row[3]

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                print(f'{username} user does not exist (skipping)')
                continue

            try:
                student = user.role
            except:
                print(f'{username} student does not exist (skipping)')
                continue

            lab_grade, created = LabGrade.objects.get_or_create(
                offering=offering,
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

def update_status(push):
    offering_slug = settings.CS111_OFFERING
    offering = Offering.objects.get(slug=offering_slug)

    repo = push.repo
    repo_path = repo.path
    upstream_repo_path = f'{offering_slug}/jon/cs111'
    if repo_path == upstream_repo_path:
        for role in Role.objects.filter(offering=offering, role=Role.STUDENT):
            username = role.user.username
            try:
                repo = Repo.objects.get(path=f'{offering_slug}/{username}/cs111')
            except Repo.DoesNotExist:
                continue
            upstream_status, created = UpstreamStatus.objects.get_or_create(
                repo=repo, defaults={'is_merged': False}
            )
            if not created:
                upstream_status.is_merged = False
                upstream_status.save()
        return

    if repo_path == f'{offering_slug}/jon/cs111-grades' and push.refname == 'refs/heads/main':
        update_grades(push)
        return

    parts = repo_path.split('/')
    if len(parts) != 3:
        return
    elif parts[0] != offering_slug:
        return
    elif parts[2] != 'cs111':
        return

    try:
        role = Role.objects.get(offering=offering, role=Role.STUDENT, user__username=parts[1])
    except Role.DoesNotExist:
        return

    upstream_repo = Repo.objects.get(path=upstream_repo_path)
    latest_commit = upstream_repo.pushes.filter(refname='refs/heads/main').latest('time').new_rev

    git_path = os.path.join(home_dir(), 'repositories', f'{repo_path}.git')

    sudo_cmd = ['sudo', '-n', '-u', settings.GITOLITE_USER]
    result = subprocess.run(sudo_cmd + ['git', 'branch', 'main', '--contains', latest_commit],
                            cwd=git_path, capture_output=True)
    if result.returncode == 0:
        is_merged = True
    else:
        is_merged = False
    
    upstream_status, created = UpstreamStatus.objects.get_or_create(
        repo=repo, defaults={'is_merged': is_merged}
    )
    if not created:
        upstream_status.is_merged = is_merged
        upstream_status.save()

    if not is_merged:
        return

    result = subprocess.run(sudo_cmd + ['git', 'diff', '--name-status', latest_commit, push.new_rev],
                            cwd=git_path, capture_output=True, text=True)
    labs_modified = set()
    for line in result.stdout.splitlines():
        s, p = line.split('\t')
        if s != 'M':
            continue
        if '/' in p and p.split('/')[0].startswith('lab'):
            labs_modified.add(p.split('/')[0])
    for lab in Lab.objects.filter(offering=offering):
        is_modified = f'lab{lab.number}' in labs_modified
        submission_status, created = SubmissionStatus.objects.get_or_create(
            repo=repo, lab=lab, defaults={'is_modified': is_modified}
        )
        if not created:
            submission_status.is_modified = is_modified
            submission_status.save()
