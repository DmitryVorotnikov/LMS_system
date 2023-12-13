import os

from celery import Celery

# Устанавливаем модуль настроек Django по умолчанию для программы 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('LMS_system')

# Использование строки здесь означает, что рабочему не нужно сериализовать
# объект конфигурации для дочерних процессов.
# - namespace='CELERY' означает, что все ключи конфигурации, связанные с Celery,
#   должны иметь префикс `CELERY_`.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузка модулей задач из всех зарегистрированных приложений Django.
app.autodiscover_tasks()
