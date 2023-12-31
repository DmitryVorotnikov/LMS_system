# Generated by Django 4.2.7 on 2023-12-10 20:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0007_alter_payment_link_for_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Создатель платежа'),
        ),
    ]
