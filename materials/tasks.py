from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from materials.services import send_email
from users.models import User


@shared_task
def subscription_send_mail(course, users):
    send_email(course, users)


@shared_task
def check_last_session():
    current_date = timezone.now()
    four_months_ago = current_date - timedelta(days=120)

    for user in User.objects.all():
        if user.last_login < four_months_ago:
            user.is_active = False
            user.save()
