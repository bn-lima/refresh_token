from django.urls import path
from .views import RegisterAccount, LoginAccount, CheckAuthentication, RefreshTokenView

urlpatterns = [
    path("register/", RegisterAccount.as_view(), name="register"), # Registra usuário
    path("login/", LoginAccount.as_view(), name="login"), # Realiza login
    path("refresh_token/", RefreshTokenView.as_view(), name="refresh"),
    path("test_authentication/", CheckAuthentication.as_view(), name="test_authentication")
]