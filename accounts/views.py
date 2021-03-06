from django.shortcuts import render
from django.http.response import JsonResponse
from .serializer import AccountsSerializer
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from .serializer import AccountsSerializer
from knox.views import LoginView
from knox.models import AuthToken
from django.contrib.auth import authenticate


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

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def logout(self, request, *args, **kwargs):
        request._auth.delete()
        return JsonResponse({"message": "logout"})

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def check_token(self, request, *args, **kwargs):
        return JsonResponse({"token": True})

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def get_user(self, request, *args, **kwargs):
        user = request._auth.user
        response = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
        }
        return JsonResponse(response)
