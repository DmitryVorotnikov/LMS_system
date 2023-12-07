from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from education.models import Lesson, Course
from users.models import User


class MyTestHelper:
    """
    Класс MyTestHelper содержит методы, которые упрощают работу с тестами и уменьшают объем кода.
    The MyTestHelper class contains methods that simplify working with tests and reduce code duplication.
    """

    @staticmethod
    def create_user():
        """
        Создает пользователя с заданными параметрами для использования в тестах.
        Creates a user with specified parameters for use in tests.
        """
        user = User.objects.create(
            email='user@test.com',
            password='test',
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        # Присвоение и хэширование пароля.
        # Password assignment and hashing.
        user.set_password('123456789')
        user.save()
        return user

    @staticmethod
    def create_auth_client(user):
        """
        Создает аутентифицированный клиент API для указанного пользователя.
        Creates an authenticated API client for the given user.
        """
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    @staticmethod
    def create_new_obj_and_get_pk(client, url, data):
        """
        Создает новый объект и возвращает id (primary key) нового объекта.
        Creates a new object and returns the id (primary key) of the new object.
        """
        new_response = client.post(
            url,
            data=data
        )
        return new_response.data['id']


class CourseStatusCodeTestCase(APITestCase):
    """
    Тесты статуса кодов CourseViewSet от всех HTTP-запросов.
    """

    def setUp(self) -> None:
        # Создаем пользователя.
        self.user = MyTestHelper.create_user()
        # Проходим аутентификацию пользователем.
        self.client = MyTestHelper.create_auth_client(self.user)

        self.url = reverse('education:courses-list')
        self.data = {
            'name': 'Course test data'
        }

    def test_course_post(self):
        """
        Тестирование статуса кода при создании курса.
        """
        response = self.client.post(
            self.url,
            data=self.data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_course_get_list(self):
        """
        Тестирование статуса кода при запросе списка курсов.
        """
        response = self.client.get(self.url)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_course_get_detail(self):
        """
        Тестирование статуса кода при запросе одного курса.
        """
        course_id = MyTestHelper.create_new_obj_and_get_pk(client=self.client, url=self.url, data=self.data)

        detail_url = reverse('education:courses-detail', kwargs={'pk': course_id})
        response = self.client.get(detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_course_put(self):
        """
        Тестирование статуса кода при частичном обновлении курса.
        """
        course_id = MyTestHelper.create_new_obj_and_get_pk(client=self.client, url=self.url, data=self.data)

        detail_url = reverse('education:courses-detail', kwargs={'pk': course_id})
        response = self.client.put(
            detail_url,
            data=self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_course_patch(self):
        """
        Тестирование статуса кода при обновлении курса.
        """
        course_id = MyTestHelper.create_new_obj_and_get_pk(client=self.client, url=self.url, data=self.data)

        detail_url = reverse('education:courses-detail', kwargs={'pk': course_id})
        response = self.client.patch(
            detail_url,
            data=self.data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_course_delete(self):
        """
        Тестирование статуса кода при удалении курса.
        """
        course_id = MyTestHelper.create_new_obj_and_get_pk(client=self.client, url=self.url, data=self.data)

        detail_url = reverse('education:courses-detail', kwargs={'pk': course_id})
        response = self.client.delete(detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class LessonStatusCodeTestCase(APITestCase):
    """
    Тесты статуса кодов всех LessonsAPIView.
    """

    def setUp(self) -> None:
        # Создаем пользователя.
        self.user = MyTestHelper.create_user()
        # Проходим аутентификацию пользователем.
        self.client = MyTestHelper.create_auth_client(self.user)

        # Сохраняем данные для курса.
        self.url_for_course = reverse('education:courses-list')
        self.data_for_course = {
            'name': 'Course test data',
        }

        # Создаем курс и получаем id курса.
        course_id = MyTestHelper.create_new_obj_and_get_pk(client=self.client, url=self.url_for_course,
                                                           data=self.data_for_course)

        # Сохраняем данные для урока.
        self.url_create = reverse('education:lessons_create')
        self.data_for_lesson = {
            'name': 'lessons test data',
            'course': course_id
        }

    def test_lesson_create(self):
        """
        Тестирование статуса кода при создании урока.
        """
        response = self.client.post(
            self.url_create,
            data=self.data_for_lesson
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_lesson_list(self):
        """
        Тестирование статуса кода при просмотре списка уроков.
        """
        response = self.client.get(
            reverse('education:lessons_list'),
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_retrieve(self):
        """
        Тестирование статуса кода при запросе одного урока.
        """
        lesson_id = MyTestHelper.create_new_obj_and_get_pk(self.client, self.url_create, self.data_for_lesson)

        detail_url = reverse('education:lessons_get', kwargs={'pk': lesson_id})
        response = self.client.get(detail_url)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_update(self):
        """
        Тестирование статуса кода при обновлении урока.
        """
        lesson_id = MyTestHelper.create_new_obj_and_get_pk(self.client, self.url_create, self.data_for_lesson)

        detail_url = reverse('education:lessons_update', kwargs={'pk': lesson_id})
        response = self.client.put(
            detail_url,
            data=self.data_for_lesson
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_delete(self):
        """
        Тестирование статуса кода при удалении урока.
        """
        lesson_id = MyTestHelper.create_new_obj_and_get_pk(self.client, self.url_create, self.data_for_lesson)

        detail_url = reverse('education:lessons_delete', kwargs={'pk': lesson_id})
        response = self.client.delete(detail_url)

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionStatusCodeTestCase(APITestCase):
    """
    Тесты статуса кодов всех SubscriptionAPIView.
    """

    def setUp(self) -> None:
        # Создаем пользователя.
        self.user = MyTestHelper.create_user()
        # Проходим аутентификацию пользователем.
        self.client = MyTestHelper.create_auth_client(self.user)

        # Сохраняем данные для курса.
        self.url_for_course = reverse('education:courses-list')
        self.data_for_course = {
            'name': 'Course test data',
        }

        # Создаем курс и получаем id курса.
        course_id = MyTestHelper.create_new_obj_and_get_pk(client=self.client, url=self.url_for_course,
                                                           data=self.data_for_course)

        # Сохраняем данные для подписки.
        self.url_create = reverse('education:subs_create')
        self.data_for_subscription = {
            'user': self.user.id,
            'course': course_id
        }

    def test_subscription_create(self):
        """
        Тестирование статуса кода при создании подписки.
        """
        response = self.client.post(
            self.url_create,
            data=self.data_for_subscription
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_subscription_delete(self):
        """
        Тестирование статуса кода при удалении подписки.
        """
        subscription_id = MyTestHelper.create_new_obj_and_get_pk(self.client, self.url_create,
                                                                 self.data_for_subscription)

        detail_url = reverse('education:subs_delete', kwargs={'pk': subscription_id})
        response = self.client.delete(detail_url)

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class LessonListTestCase(APITestCase):
    """
    Тест просмотра списка Уроков.
    """

    def setUp(self) -> None:
        # Создаем пользователя.
        self.user = MyTestHelper.create_user()
        # Проходим аутентификацию пользователем.
        self.client = MyTestHelper.create_auth_client(self.user)

        # Сохраняем данные для курса.
        self.url_for_course = reverse('education:courses-list')
        self.data_for_course = {
            'name': 'Course test data',
        }

        # Создаем курс и получаем id курса.
        course_id = MyTestHelper.create_new_obj_and_get_pk(client=self.client, url=self.url_for_course,
                                                           data=self.data_for_course)

        # Сохраняем данные для урока.
        # self.url_for_lesson_list = reverse('education:lessons_list')
        self.data_for_lesson = {
            'course': course_id,
            'name': 'Lesson test data',
        }

        # Создаем Урок.
        self.lesson = Lesson.objects.create(
            course=Course.objects.get(pk=course_id),
            name=self.data_for_lesson.get('name')
        )

    def test_lesson_list(self):
        """
        Тестирование просмотра списка уроков.
        """
        response = self.client.get(
            '/lessons/',  # Или self.url_for_lesson_list
        )

        self.assertEquals(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.id,
                        "link_to_video": None,
                        "name": self.lesson.name,
                        "description": None,
                        "preview": None,
                        "course": self.lesson.course_id
                    }
                ]
            }
        )
