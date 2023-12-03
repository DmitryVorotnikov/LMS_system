from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from education.models import Course, Lesson
from education.permissions import CourseSetPermission
from education.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [CourseSetPermission]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    # Метод укажет текущего пользователя как создателя курса.
    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.creator = self.request.user
        new_course.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        # Обычному пользователю показываем только созданные им курсы.
        if not self.request.user.is_staff:
            user_id = self.request.user.id
            queryset = self.queryset.filter(creator=user_id)
        return queryset


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ~IsAdminUser]
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            # Обычному пользователю показываем только уроки из созданных им курсов.
            user_id = self.request.user.id
            return Lesson.objects.filter(course__creator=user_id)

        return Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            # Обычному пользователю показываем только уроки из созданных им курсов.
            user_id = self.request.user.id
            return Lesson.objects.filter(course__creator=user_id)

        return Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            # Обычному пользователю показываем только уроки из созданных им курсов.
            user_id = self.request.user.id
            return Lesson.objects.filter(course__creator=user_id)

        return Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, ~IsAdminUser]

    def get_queryset(self):
        if not self.request.user.is_staff:
            # Обычному пользователю показываем только уроки из созданных им курсов.
            user_id = self.request.user.id
            return Lesson.objects.filter(course__creator=user_id)

        return Lesson.objects.all()
