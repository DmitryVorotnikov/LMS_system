from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from education.models import Course, Lesson, Subscription
from education.paginators import CoursePaginator, LessonPaginator
from education.permissions import CourseSetPermission
from education.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


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
    permission_classes = [IsAuthenticated, ~IsAdminUser]
    serializer_class = LessonSerializer


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
