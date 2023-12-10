import stripe
from django.conf import settings


# Потом удалю, это для проверяющего
# sk_test_51OLqKkASwLHByYrPWC8v5hJYJ8FZbmUWYOFKh3jdhdgDB8YTaf8P9I60FGCyEIuurenvY16yZbsXlak2CoFxOwk600SJhjsHEU

def get_link_for_payment(paid_course, payment_amount):
    stripe.api_key = settings.STRIPE_API_KEY

    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f'Course {paid_course}',
                },
                'unit_amount': payment_amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000',
        cancel_url='http://localhost:8000',
    )

    return session.url, session.id


def check_payment_status(payment_session_id):
    stripe.api_key = settings.STRIPE_API_KEY

    response = stripe.checkout.Session.retrieve(id=payment_session_id)

    return response.status
