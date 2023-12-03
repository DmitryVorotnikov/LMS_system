from rest_framework import serializers

ALLOWED_LINKS = ['youtube']


def validator_link_to_video(value):
    """
    Валидатор проверяет, что ссылка входит в список разрешенных ресурсов.
    """
    if not set(value.lower().split('.')) & set(ALLOWED_LINKS):
        error_message = 'Использована запрещенная ссылка!'
        raise serializers.ValidationError(error_message)

