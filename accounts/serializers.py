from rest_framework import serializers
from .models import Account
from .validators import PASSWORD_VALIDATOR
from .services import authenticate_account
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class RegisterAccountSerializer(serializers.ModelSerializer): # Serializer responsável por registrar um usuário
    confirm_password = serializers.CharField(max_length=128, required=True) # Campo para confirmar senha
    
    class Meta:
        model = Account
        fields = ("username", "password", "confirm_password")

        extra_kwargs = {
            "confirm_password": {
                "validators": [PASSWORD_VALIDATOR]
            }
        }

    def validate(self, data):
        
        if data.get("password") != data.get("confirm_password"): # Retorna erro caso as senhas não sejam iguais
            raise serializers.ValidationError("Passwords do not match")
        
        return data
    
    def create(self, validated_data): # Cria usuário
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")

        user = Account.objects.create(**validated_data)
        user.set_password(password) # Seta senha de forma segura
        user.save()

        return user
    
class LoginAccountSerializer(serializers.Serializer): # Serializer responsável por logar o usuário
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True)

    def validate(self, data):
        
        token_pair = authenticate_account(data.get("username"), data.get("password")) # Valida se existe um usuário com as credenciais enviadas

        if not token_pair: # Retorna erro caso não exista usuário
            raise serializers.ValidationError("Invalid credentials")
        
        data["token_pair"] = token_pair
        return data
    
    def save(self, **kwargs): # Devolve token de acesso
        return self.validated_data.get("token_pair")
    
class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate(self, data):
        try:
            refresh_token = RefreshToken(data.get("refresh_token"))
        except TokenError:
            raise serializers.ValidationError("Invalid or expired refresh_token")
        
        data["new_access_token"] = str(refresh_token.access_token)
        return data
    
    def save(self, **kwargs):
        return self.validated_data.get("new_access_token")