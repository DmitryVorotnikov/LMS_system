from django.db import models

from education.models import Course
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Payment(models.Model):
    # Класс для CHOICES способа оплаты.
    class PaymentType(models.TextChoices):
        CASH = 'CASH', 'Наличные'
        TR_TO_ACC = 'TR_TO_ACC', 'Перевод на счет'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс')
    date_of_payment = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    payment_amount = models.PositiveIntegerField(verbose_name='Сумма оплаты', **NULLABLE)
    payment_type = models.CharField(max_length=25, choices=PaymentType.choices, default=PaymentType.CASH,
                                    verbose_name='Способ оплаты')

    def __str__(self):
        return f'Платеж от {self.user}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('-date_of_payment',)
