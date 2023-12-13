# LMS-system (ENG)

## Description

The project is an application for managing educational courses within a Learning Management System (LMS). The application provides a fully functional REST API for handling courses, users, and payments.

## Technologies and Tools

- Used technologies: Python, Django, Django REST Framework, drf-yasg, Stripe.
- Authorization is done through the JWT (JSON Web Tokens) mechanism.
- The user model is overridden to separate roles and assign different permission classes.
- API documentation is available through Swagger and ReDoc following the OpenAPI specification.
- Endpoint tests have been written.
- Integration with a third-party API: Stripe payment system.
- Asynchronous tasks are employed via Celery and Celery-beat with a Redis broker for deferred and periodic tasks.
- Features for automatic email sending have been configured.
- CORS settings are enabled to ensure security.

## Data Models

- Course model
- Lesson model for courses
- Subscription model for course subscriptions
- Payment model
- User model

## Functionality

The application allows:

- Creation of courses and lessons
- Subscribing to courses
- Purchasing courses
- Learning and undergoing training within the created courses

- Documentation for available endpoints will be accessible through Swagger after project launch.



# LMS-system (RUS)

## Описание

Проект представляет собой приложение для управления учебными курсами в системе управления обучением (LMS). Приложение
предоставляет полностью функциональный REST API для работы с курсами, пользователями и платежами.

## Технологии и инструменты

- Используемые технологии: Python, Django, Django REST Framework, drf-yasg, Stripe.
- Авторизация осуществляется через механизм JWT (JSON Web Tokens).
- Модель пользователя переопределена для разделения ролей и назначения различных классов разрешений.
- Документация API доступна через Swagger и ReDoc по спецификации OpenAPI.
- Написаны тесты для эндпоинтов.
- Интеграция стороннего API: платежная система Stripe.
- Используются асинхронные задачи через Celery и Celery-beat с брокером Redis для отложенных и периодических задач.
- Настроены функции для автоматической отправки почты.
- Включены настройки CORS для обеспечения безопасности.

## Модели данных

- Модель курса (Course)
- Модель урока для курса (Lesson)
- Модель подписки на курсы (Subscription)
- Модель платежа (Payment)
- Модель пользователя (User)

## Функциональность

Приложение позволяет:

- Создавать курсы и уроки
- Подписываться на курсы
- Осуществлять покупку курсов
- Учиться и проходить обучение по созданным курсам

- Документация по доступным эндпоинтам будет доступна через Swagger после запуска проекта.
