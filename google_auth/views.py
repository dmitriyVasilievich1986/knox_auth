from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from urllib.parse import urlencode
from knox.models import AuthToken
from uuid import uuid4
from os import environ
import requests

REDIRECT_URI = environ.get("REDIRECT_URI", "http://localhost:80/auth/google_callback/")
CLIENT_SECRET = environ.get("CLIENT_SECRET")
CLIENT_ID = environ.get("CLIENT_ID")


def get_google_url(request, *args, **kwargs):
    state = str(uuid4())
    params = {
        "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "duration": "temporary",
        "client_id": CLIENT_ID,
        "state": state,
    }
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
    return JsonResponse({"url_string": url})


def google_callback_veiw(request, *args, **kwargs):
    error = request.GET.get("error", "")
    if error:
        return "Error: " + error
    code = request.GET.get("code", "")
    token = get_token(code)
    profile = get_profile(token)
    email = profile.get("email", None)
    user = User.objects.filter(email=email).first()
    if user is None:
        user = User(
            username=email,
            first_name=profile.get("given_name", ""),
            last_name=profile.get("family_name", ""),
            email=email,
        )
        user.save()
    _, knox_token = AuthToken.objects.create(user)
    return redirect(f"/oauth?token={knox_token}")


def g(request, *args, **kwargs):
    token = request.GET.get("token", "")
    return JsonResponse({"token": token})


def get_token(code, *args, **kwargs):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }
    response = requests.post(
        "https://www.googleapis.com/oauth2/v4/token", auth=client_auth, data=post_data
    )
    token_json = response.json()
    return token_json["access_token"]


def get_profile(access_token, *args, **kwargs):
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo", headers=headers
    )
    me_json = response.json()
    return me_json
