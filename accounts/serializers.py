from rest_framework import serializers
from .models import Account
from .validators import PASSWORD_VALIDATOR
from .services import authenticate_account, revoke_user_refresh_tokens
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class RegisterAccountSerializer(serializers.ModelSerializer): # Serializer responsável por registrar um usuário
    confirm_password = serializers.CharField(max_length=128, required=True) # Campo para confirmar senha
    
    class Meta:
        model = Account
        fields = ("email", "password", "confirm_password")

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
    email = serializers.EmailField(max_length=350, required=True)
    password = serializers.CharField(max_length=128, required=True)

    def validate(self, data):
        
        token_pair = authenticate_account(data.get("email"), data.get("password")) # Valida se existe um usuário com as credenciais enviadas

        if not token_pair: # Retorna erro caso não exista usuário
            raise serializers.ValidationError("Invalid credentials")
        
        data["token_pair"] = token_pair
        return data
    
    def save(self, **kwargs): # Devolve token de acesso
        return self.validated_data.get("token_pair")
    
class RefreshTokenSerializer(serializers.Serializer): # Serializer responsável por gerar um novo token de acesso a partir de um refresh token
    refresh_token = serializers.CharField(required=True)

    def validate(self, data):
        try:
            refresh_token = RefreshToken(data.get("refresh_token")) # Valida o refresh token enviado
        except TokenError:
            raise serializers.ValidationError("Invalid or expired refresh_token")
        
        data["new_access_token"] = str(refresh_token.access_token) # Gera um novo token de acesso
        return data
    
    def save(self, **kwargs):
        return self.validated_data.get("new_access_token") # Retorna o novo token de acesso
    
class ChangePasswordSerializer(serializers.Serializer): # Serializer responsável por validar e alterar a senha do usuário
    current_password = serializers.CharField(max_length=128, required=True, validators=[PASSWORD_VALIDATOR])
    new_password = serializers.CharField(max_length=128, required=True, validators=[PASSWORD_VALIDATOR])
    confirm_new_password = serializers.CharField(max_length=128, required=True, validators=[PASSWORD_VALIDATOR])

    def validate(self, data):
        user = self.context.get("user")

        if not user.check_password(data.get("current_password")): # Verifica se a senha atual está correta
            raise serializers.ValidationError("Current password is incorrect")
        
        if user.check_password(data.get("new_password")): # Verifica se a nova senha é diferente da senha atual
            raise serializers.ValidationError("The new password cannot be the same as your current password")
        
        if data.get("confirm_new_password") != data.get("new_password"): # Verifica se as novas senhas são iguais
            raise serializers.ValidationError("Passwords do not match")
        
        return data
    
    def save(self, **kwargs):

        user = self.context.get("user")
        user.set_password(self.validated_data.get("new_password")) # Define a nova senha de forma segura

        revoke_user_refresh_tokens(user) # Invalida todos os refresh tokens do usuário

        return user.save()