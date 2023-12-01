from rest_framework.permissions import BasePermission


class UserUpdateDeletePermission(BasePermission):
    """
    Разрешаем пользователю редактирование и удаление только собственного профиля.
    """

    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
