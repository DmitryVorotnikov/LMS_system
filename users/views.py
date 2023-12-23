from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.permissions import UserUpdateDeletePermission
from users.serializers import UserSerializer, UserForAdminSerializer, UserForUserSerializer


class UserCreateAPIView(generics.CreateAPIView):

    def get_serializer_class(self):
        if self.request.user.is_staff:
            # Если is_staff=True, то можно создать любого пользователя.
            return UserForAdminSerializer

        return UserSerializer


class UserListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            # Если is_staff=True, то показываем информацию подробно.
            return UserForAdminSerializer

        # Если обычный пользователь, то показываем информацию кратко.
        return UserForUserSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            # Если is_staff=True, то показываем информацию подробно.
            return UserForAdminSerializer

        # Если обычный пользователь, то показываем информацию кратко.
        return UserForUserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, UserUpdateDeletePermission]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            # Если is_staff=True, то можно редактировать все поля.
            return UserForAdminSerializer

        return UserSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, UserUpdateDeletePermission]
    queryset = User.objects.all()
