from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from education.models import Course
from users.models import User


def send_mail_to_subscribers(course):
    # Получаем подписчиков курса.
    # Фильтр: Пользователи, на которых ссылается Подписка, у которой есть ссылка на конкретный Курс.
    subscribers = User.objects.filter(subscription__course=course)

    for user in subscribers:
        send_mail(
            subject='Обновление курса!',
            message='Курс на который вы подписались был недавно обновлен, заходи на сайт, учись!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )



@shared_task
def task_check_is_update(id):
    course = Course.objects.get(id=id)

    # Получаем текущее время.
    current_datetime = timezone.now()

    # Если время последнего обновления = None, то это первый урок курса и отправляем письмо.
    if not course.is_update:
        send_mail_to_subscribers(course)

    # Проверяем, что время последнего обновления курса старше, чем текущее время на 4 часа и отправляем письмо.
    elif course.is_update < current_datetime - timedelta(hours=4):
        send_mail_to_subscribers(course)


@shared_task
def task_monthly_user_blocking():
    # Определяем дату, которая была месяц назад от текущего момента.
    month_ago = timezone.now() - timedelta(days=30)

    # Словарь для фильтра.
    filter_last_login = {'last_login__lt': month_ago, 'is_active': True, 'is_staff': False}

    users = User.objects.filter(**filter_last_login)

    # Блокируем сразу всех пользователей.
    users.update(is_active=False)

    # for user in users:
    #     user.is_active = False
    #     user.save()
