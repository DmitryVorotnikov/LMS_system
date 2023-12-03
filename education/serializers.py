from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from education.models import Course, Lesson
from education.validators import validator_link_to_video


class LessonSerializer(serializers.ModelSerializer):
    # Валидатор для ссылок на видео.
    link_to_video = serializers.URLField(
        validators=[validator_link_to_video],
        required=False,  # Делаем поле снова не обязательным.
        allow_blank=True,
        allow_null=True
    )

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
