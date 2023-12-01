from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from education.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lesson_set.count', default=0, read_only=True)
    # Поле для отображения уроков в get-запрос на курсы.
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
