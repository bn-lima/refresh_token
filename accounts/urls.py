from django.urls import path
from .views import RegisterAccount, LoginAccount, TestAuthentication

urlpatterns = [
    path("register/", RegisterAccount.as_view(), name="register"), # Registra usuário
    path("login/", LoginAccount.as_view(), name="login"), # Realiza login
    path("test_authentication/", TestAuthentication.as_view(), name="test_authentication")
]