import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        admin = User.objects.create(
            email=os.getenv('SU_EMAIL'),
            first_name='admin',
            last_name='online_education',

            is_staff=True,
            is_active=True,
            is_superuser=True,
        )
        admin.set_password(os.getenv('SU_PASS'))
        admin.save()
