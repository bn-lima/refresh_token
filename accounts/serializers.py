from rest_framework import serializers
from .models import Account
from .validators import PASSWORD_VALIDATOR
from .services import authenticate_account

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
        
        token = authenticate_account(data.get("username"), data.get("password")) # Valida se existe um usuário com as credenciais enviadas

        if not token: # Retorna erro caso não exista usuário
            raise serializers.ValidationError("Invalid credentials")
        
        data["access_token"] = token.key
        return data
    
    def save(self, **kwargs): # Devolve token de acesso
        return self.validated_data.get("access_token")