from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from education.models import Course, Lesson
from education.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    # Устанавливаем разные разрешения в зависимости от метода запроса.
    def get_permissions(self):
        # Создавать и удалять курсы может любой авторизованный пользователь, кроме is_staff=True.
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAuthenticated, ~IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ~IsAdminUser]
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, ~IsAdminUser]
    queryset = Lesson.objects.all()
