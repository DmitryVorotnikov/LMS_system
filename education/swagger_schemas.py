from drf_yasg import openapi


# Здесь храниться пример для ручного документирования представлений,
# Он может быть импортирован в представление и там использоваться.
def lesson_create_schema():
    return {
        'operation_description': "Описание представления, аналогичное обычному докстрингу представления.",
        'request_body': openapi.Schema(  # Описание request.
            type=openapi.TYPE_OBJECT,
            properties={  # Описание полей.
                'course': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID курса'
                ),
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Название урока',
                    maxLength=150,
                    minLength=1
                ),
                'description': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Описание урока',
                    nullable=True
                ),
                'preview': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_BINARY,
                    description='Превью изображение',
                    nullable=True
                ),
                'link_to_video': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_URI,
                    description='Ссылка на видео',
                    nullable=True
                ),
            },
            required=['course', 'name'],  # Указываем обязательные поля.
            title='Lesson',  # Указываем заголовок, можно указать название модели.
        ),
        'responses': {  # Описание ожидаемого responses.
            201: openapi.Schema(  # Ожидаем статус-код 201.
                type=openapi.TYPE_OBJECT,
                properties={  # Описание полей.
                    'id': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='ID урока',
                        read_only=True
                    ),
                    'course': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='ID курса'
                    ),
                    'name': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Название урока',
                        maxLength=150,
                        minLength=1
                    ),
                    'description': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Описание урока',
                        nullable=True
                    ),
                    'preview': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_BINARY,
                        description='Превью изображение',
                        nullable=True
                    ),
                    'link_to_video': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_URI,
                        description='Ссылка на видео',
                        nullable=True
                    ),
                },
                title='Lesson',  # Указываем заголовок, можно указать название модели.
            ),
        },
    }
