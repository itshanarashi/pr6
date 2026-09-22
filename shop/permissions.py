from rest_framework.permissions import BasePermission, SAFE_METHODS


class ApiAccessPermission(BasePermission):
    """Чтение доступно всем, изменение данных — только сотрудникам."""

    message = 'Для изменения данных необходима учетная запись сотрудника.'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
