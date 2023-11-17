from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        moderator = User.objects.create(
            email='moderator@mail.ru',
            first_name='moderator1',
            last_name='moderator1',
            role='moderator',

            is_active=True,
        )

        moderator.set_password('qwe123')
        moderator.save()