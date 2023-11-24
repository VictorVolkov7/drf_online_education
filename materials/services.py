import os

import stripe
from django.conf import settings
from django.core.mail import send_mail


def stripe_payment_created(material_name, material_price, user):
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    product = stripe.Product.create(
        name=material_name,
    )

    price = stripe.Price.create(
        unit_amount=material_price,
        currency="usd",
        product=product['id'],
    )

    session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[
            {
                "price": price.id,
                "quantity": 1,
            },
        ],
        mode="payment",
        client_reference_id=user,
    )
    return session


def send_email(course, users):
    send_mail(
        subject=f'Курс {course} обновлен',
        message='Произошло обновление курса, зайдите и посмотрите!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[users],
    )
