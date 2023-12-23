from django.contrib.auth.hashers import make_password


def password_hashing_on_creation(validated_data):
    """
    Hashes the user's password before saving it to the DB.
    Хеширует пароль пользователя перед записью в БД.
    """
    # Получение пароля из переданных данных.
    password = validated_data.get('password')

    # Хеширование пароля.
    hashed_password = make_password(password)

    # Замена пароля на хешированный в переданных данных.
    validated_data['password'] = hashed_password

    # Создание пользователя с обновленными данными.
    return validated_data


def password_hashing_on_update(validated_data):
    """
    Hashes the user's password before saving it to the DB.
    Хеширует пароль пользователя перед записью в БД.
    """
    # Получение пароля из запроса.
    password = validated_data.get('password')

    # Хеширование пароля, если он был изменен.
    if password:
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password

    return validated_data
