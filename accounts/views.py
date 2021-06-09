# region import libraries
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .serializer import AccountsSerializer
from knox.models import AuthToken

from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework import permissions

# endregion


class AccountsViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    # region Create
    def create(self, request, *args, **kwargs):
        serializer = AccountsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({**serializer.data, "token": token})

    @action(detail=False, methods=["POST"])
    def login(self, request, *args, **kwargs):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        if username is None or password is None:
            raise ValidationError("Не предоставлены необходимые данные.")
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError("Пользователь не найден.")
        serializer = AccountsSerializer(user)
        _, token = AuthToken.objects.create(user)
        return Response({**serializer.data, "token": token})

    # endregion

    # region Read
    def list(self, request, *args, **kwargs):
        instance = request._auth and request._auth.user
        if instance is None:
            raise ValidationError("Invalid token")
        serializer = AccountsSerializer(instance)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        return Response({"message": "Bad request"})

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def check_token(self, request, *args, **kwargs):
        return Response({"token": True})

    # endregion

    # region Update
    def update(self, request, *args, **kwargs):
        instance = request._auth and request._auth.user
        if instance is None:
            raise ValidationError("Invalid token")
        serializer = AccountsSerializer(
            instance=instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # endregion

    # region Delete
    def destroy(self, request, *args, **kwargs):
        instance = request._auth and request._auth.user
        if instance is None:
            raise ValidationError("Invalid token")
        request._auth.delete()
        return Response({"message": "logout"})

    # endregion
