from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializers import RegisterAccountSerializer, LoginAccountSerializer, RefreshTokenSerializer
from rest_framework.response import Response

class RegisterAccount(APIView): # View responsável por registrar um usuário
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        
        serializer = RegisterAccountSerializer(data=request.data) # Serializer responsável por registrar usuário
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Account created successfully"}, status=status.HTTP_200_OK)
    
class LoginAccount(APIView): # View responsável por logar o usuário
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_pair = serializer.save()

        return Response({"token_pair": token_pair}, status=status.HTTP_200_OK)
    
class CheckAuthentication(APIView): # Verifica se o usuário está logado
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"detail": "You are authenticated!"}, status=status.HTTP_200_OK)
    
class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_access_token = serializer.save()

        return Response({"new_access_token": new_access_token}, status=status.HTTP_200_OK)