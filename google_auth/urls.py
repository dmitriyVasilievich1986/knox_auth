from django.urls import path
from .views import google_callback_veiw, get_google_url


urlpatterns = [
    path("get_google_url/", get_google_url),
    path("google_callback/", google_callback_veiw),
]
