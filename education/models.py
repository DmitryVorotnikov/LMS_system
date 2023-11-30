from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    preview = models.ImageField(upload_to='education/preview/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('id',)


class Lesson(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс')
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='education/preview/', verbose_name='Превью', **NULLABLE)
    link_to_video = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)


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
