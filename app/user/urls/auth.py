from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from ..views import (CustomObtainTokenPairView,
                     TokenDecode,PasswordChangeView)

app_name = "auth"
router = DefaultRouter()
router.register("change-password", PasswordChangeView, basename="password-change")

urlpatterns = [
    path("login/", CustomObtainTokenPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("token/verify/", TokenVerifyView.as_view(), name="verify-token"),
    path("decode", TokenDecode.as_view(), name='token-decode'),
    path("", include(router.urls)),
]


