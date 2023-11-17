from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        member = User.objects.create(
            email='test@mail.ru',
            first_name='member1',
            last_name='memberov1',

            is_active=True,
        )

        member.set_password('qwe123')
        member.save()
