from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from education.models import Course, Lesson, Subscription
from education.paginators import CoursePaginator, LessonPaginator
from education.permissions import CourseSetPermission
from education.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from education.tasks import task_check_is_update


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseSetPermission]
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator
    queryset = Course.objects.all()

    # Метод укажет текущего пользователя как создателя курса.
    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.creator = self.request.user
        new_course.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        # Обычному пользователю в queryset указываем его курсы.
        if not self.request.user.is_staff:
            user_id = self.request.user.id
            queryset = self.queryset.filter(creator=user_id)
        return queryset


class LessonCreateAPIView(generics.CreateAPIView):

    @swagger_auto_schema(
        operation_description="Описание представления, аналогичное обычному докстрингу представления.",
        request_body=openapi.Schema(  # Описание request.
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
        responses={  # Описание ожидаемого responses.
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
    )
    # КОД РУЧНОГО ДОКУМЕНТИРОВАНИЯ МОЖНО ВЫНЕСТИ В ОТДЕЛЬНЫЙ ФАЙЛ!
    # @swagger_auto_schema(**lesson_create_schema())
    def post(self, request, *args, **kwargs):  # Указываем тип запроса (для ручного документирования).
        return super().post(request, *args, **kwargs)

    permission_classes = [IsAuthenticated, ~IsAdminUser]
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        new_lesson = serializer.save()

        # Получаем Курс, на который ссылается текущий урок.
        course = new_lesson.course

        # Вызываем асинхронную задачу.
        task_check_is_update.delay(course.id)

        # Обновляем поле is_update у Курса.
        course.is_update = timezone.now()

        # Сохраняем данные по Курсу.
        course.save()


class LessonListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator

    def get_queryset(self):
        if not self.request.user.is_staff:
            # Обычному пользователю в queryset указываем только уроки из созданных им курсов.
            user_id = self.request.user.id
            return Lesson.objects.filter(course__creator=user_id)

        return Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            # Обычному пользователю в queryset указываем только уроки из созданных им курсов.
            user_id = self.request.user.id
            return Lesson.objects.filter(course__creator=user_id)

        return Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            # Обычному пользователю в queryset указываем только уроки из созданных им курсов.
            user_id = self.request.user.id
            return Lesson.objects.filter(course__creator=user_id)

        return Lesson.objects.all()

    def perform_update(self, serializer):
        lesson = serializer.save()

        # Вызываем асинхронную задачу.
        task_check_is_update.delay(lesson.course_id)

        serializer.save()


class LessonDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, ~IsAdminUser]

    def get_queryset(self):
        if not self.request.user.is_staff:
            # Обычному пользователю в queryset указываем только уроки из созданных им курсов.
            user_id = self.request.user.id
            return Lesson.objects.filter(course__creator=user_id)

        return Lesson.objects.all()

    def delete(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # В queryset указываем только подписки текущего пользователя.
        user_id = self.request.user.id
        return Subscription.objects.filter(user=user_id)
