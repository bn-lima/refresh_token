from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

def authenticate_account(username, password): # Verifica se account existe no banco
    user = authenticate(username=username, password=password) # Procura por um usuário com o mesmo username e password

    if not user:
        return None
    
    token, _ = Token.objects.get_or_create(user=user) # Cria e retorna token de acesso
    return token