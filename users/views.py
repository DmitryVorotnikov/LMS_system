from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    # Метод для того чтобы не записывать пароль в чистом виде в БД, а сначала хешировать его.
    def perform_create(self, serializer):
        # Получение пароля из запроса.
        password = self.request.data.get('password')

        # Хеширование пароля.
        hashed_password = make_password(password)

        # Установка хешированного пароля в сериализатор перед сохранением в БД.
        serializer.save(password=hashed_password)


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]
