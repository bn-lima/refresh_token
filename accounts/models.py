from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import PASSWORD_VALIDATOR

class Account(AbstractUser): # Modelo que representa o usuário
    email = models.EmailField(max_length=350, unique=True)
    password = models.CharField(max_length=128, validators=[PASSWORD_VALIDATOR])
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.email)