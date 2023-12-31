from django.conf import settings
from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    preview = models.ImageField(upload_to='education/preview/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                verbose_name='Создатель', **NULLABLE)

    is_update = models.DateTimeField(verbose_name='Дата/время последнего обновления', **NULLABLE)

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


class Subscription(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    subscription_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    def __str__(self):
        return f'Подписка пользователя {self.user}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('id',)
