from django.urls import path
from .views import RegisterAccount, LoginAccount

urlpatterns = [
    path("register/", RegisterAccount.as_view(), name="register"), # Registra usuário
    path("login/", LoginAccount.as_view(), name="login")
]