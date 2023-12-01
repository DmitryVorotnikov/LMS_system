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
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # Метод для того чтобы не записывать пароль в чистом виде в БД, а сначала хешировать его.
    def perform_update(self, serializer):
        # Получение пароля из запроса.
        password = self.request.data.get('password')

        # Хеширование пароля, если он был изменен.
        if password:
            hashed_password = make_password(password)
            serializer.save(password=hashed_password)
        else:
            serializer.save()


class UserDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
