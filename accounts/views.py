# region import libraries
from django.http.response import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render

from .serializer import AccountsSerializer
from .serializer import AccountsSerializer

from knox.models import AuthToken
from knox.views import LoginView

from rest_framework.serializers import ValidationError
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework import permissions

# endregion


class AccountsViewSet(ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = AccountsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        response = {
            "first_name": serializer.validated_data.get("first_name", ""),
            "last_name": serializer.validated_data.get("last_name", ""),
            "username": serializer.validated_data.get("username", ""),
            "email": serializer.validated_data.get("email", ""),
            "token": token,
        }
        return JsonResponse(response)

    def list(self, request, *args, **kwargs):
        instance = request._auth and request._auth.user
        if instance is None:
            raise ValidationError("Invalid token")
        serializer = AccountsSerializer(instance)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        return JsonResponse({"message": "Bad request"})

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def check_token(self, request, *args, **kwargs):
        return JsonResponse({"token": True})

    @action(detail=False, methods=["POST"])
    def login(self, request, *args, **kwargs):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        if username is None or password is None:
            return JsonResponse({"message": "Bad request"})
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({"message": "Bad request"})
        _, token = AuthToken.objects.create(user)
        return JsonResponse({"token": token})

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

    def destroy(self, request, *args, **kwargs):
        instance = request._auth and request._auth.user
        if instance is None:
            raise ValidationError("Invalid token")
        request._auth.delete()
        return JsonResponse({"message": "logout"})
