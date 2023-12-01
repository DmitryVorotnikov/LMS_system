from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    phone_number = PhoneNumberField(verbose_name='Телефонный номер', **NULLABLE)
    city = models.CharField(max_length=250, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Фото пользователя', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
