# forms.py
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# from apps.esocial.choices.eventos import EVENTOS
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username", "name", "is_staff", "is_superuser",
            "is_active", "groups", "eventos")
        labels = {
            "username": "Nome do usuário",
            "name": "Nome Completo",
            "is_staff": "Acessa o sistema?",
            "is_superuser": "É administrador?",
            "is_active": "Está ativo?",
            "groups": "Grupos",
        }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            "username", "name", "is_staff", "is_superuser",
            "is_active", "groups",
            "eventos")
        labels = {
            "username": "Nome do usuário",
            "name": "Nome Completo",
            "is_staff": "Acessa o sistema?",
            "is_superuser": "É administrador?",
            "is_active": "Está ativo?",
            "groups": "Grupos",
        }


# Form geral para CRUD customizado
class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "username", "name", "is_staff", "is_superuser",
            "is_active", "groups",
            "eventos"]
        labels = {
            "username": "Nome do usuário",
            "name": "Nome Completo",
            "is_staff": "Acessa o sistema?",
            "is_superuser": "É administrador?",
            "is_active": "Está ativo?",
            "groups": "Grupos",
        }
