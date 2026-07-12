from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializers import RegisterAccountSerializer, LoginAccountSerializer
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
        access_token = serializer.save()

        return Response({"access_token": access_token}, status=status.HTTP_200_OK)