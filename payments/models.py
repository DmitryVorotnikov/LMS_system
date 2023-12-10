from django.conf import settings
from django.db import models

from education.models import Course
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Payment(models.Model):
    # Класс для CHOICES способа оплаты.
    class PaymentType(models.TextChoices):
        CASH = 'CASH', 'Наличные'
        TR_TO_ACC = 'TR_TO_ACC', 'Перевод на счет'

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                verbose_name='Создатель платежа', **NULLABLE)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс')
    date_of_payment = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания оплаты')
    payment_amount = models.PositiveIntegerField(default=1, verbose_name='Сумма оплаты')
    payment_type = models.CharField(max_length=25, choices=PaymentType.choices, default=PaymentType.CASH,
                                    verbose_name='Способ оплаты')

    payment_session_id = models.CharField(max_length=300, verbose_name='Id сессии платежа', **NULLABLE)
    link_for_payment = models.CharField(max_length=700, verbose_name='Ссылка на оплату', **NULLABLE)
    payment_status = models.CharField(default='Не оплачено', max_length=300, verbose_name='Статус платежа')

    def __str__(self):
        return f'Платеж от {self.creator}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('-date_of_payment',)
