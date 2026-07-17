from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

def authenticate_account(username, password): # Verifica se account existe no banco
    user = authenticate(username=username, password=password) # Procura por um usuário com o mesmo username e password

    if not user:
        return None

    refresh = RefreshToken.for_user(user)

    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }

def revoke_user_refresh_tokens(user): # Invalida todos os refresh tokens do usuário

    tokens = OutstandingToken.objects.filter(user=user) # Busca todos os refresh tokens registrados do usuário

    for token in tokens: # Adiciona cada refresh token à blacklist
        BlacklistedToken.objects.get_or_create(token=token)