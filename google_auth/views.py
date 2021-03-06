from django.shortcuts import render
from django.http.response import JsonResponse
from uuid import uuid4
from urllib.parse import urlencode
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from knox.models import AuthToken

CLIENT_ID = "331564647878-25bkaorept2gv0lpgeckmvfndsu5jln9.apps.googleusercontent.com"
CLIENT_SECRET = "RJjBoqXa__jAlwUAr9pLywbH"
REDIRECT_URI = "http://localhost:80/auth/google_callback/"


def get_google_url(request, *args, **kwargs):
    state = str(uuid4())
    params = {
        "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
        "state": state,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "duration": "temporary",
        "client_id": CLIENT_ID,
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
            username=f"user{User.objects.all().count()}",
            first_name=profile.get("given_name", ""),
            last_name=profile.get("family_name", ""),
            email=email,
        )
        user.save()
    _, knox_token = AuthToken.objects.create(user)
    return JsonResponse({"token": knox_token, "email": email})


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
