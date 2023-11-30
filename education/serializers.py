from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from education.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    # Добавлено поле для количества уроков по курсу.
    def get_lesson_count(self, instance):
        return Lesson.objects.filter(course_id=instance.id).count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
