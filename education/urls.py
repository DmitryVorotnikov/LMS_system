from django.urls import path
from rest_framework.routers import DefaultRouter

from education.apps import EducationConfig
from education.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionCreateAPIView, \
    SubscriptionDestroyAPIView

app_name = EducationConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    # URLs уроков:
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lessons_create'),
    path('lessons/', LessonListAPIView.as_view(), name='lessons_list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lessons_get'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lessons_update'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lessons_delete'),

    # URLs подписок:
    path('subs/create/', SubscriptionCreateAPIView.as_view(), name='subs_create'),
    path('subs/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subs_delete'),
]

urlpatterns += router.urls
