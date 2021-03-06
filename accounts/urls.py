from django.urls import path
from .views import AccountsViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register("accounts", AccountsViewSet, basename="accounts")

urlpatterns = router.urls
