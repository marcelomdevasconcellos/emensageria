from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# from apps.esocial.choices.eventos import EVENTOS
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username", "name", "is_staff", "is_superuser",
            "is_active", "groups")
        labels = {
            "username": "CPF",
            "name": "Nome Completo",
            "is_staff": "Acessa o sistema?",
            "is_superuser": "É administrador?",
            "is_active": "Está ativo?",
            "groups": "Grupos",
        }

    def clean_username(
            self):
        # Função para validar CPF e remover formatação
        cpf = self.cleaned_data["username"]
        cpf = User.remover_formatacao(cpf)
        # Custom validation for CPF here if needed
        if User.objects.filter(username=cpf).exists():
            raise forms.ValidationError("Um usuário com este CPF já está cadastrado.")
        return cpf


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "username", "name", "is_staff", "is_superuser",
            "is_active", "groups")
        labels = {
            "username": "CPF",
            "name": "Nome Completo",
            "is_staff": "Acessa o sistema?",
            "is_superuser": "É administrador?",
            "is_active": "Está ativo?",
            "groups": "Grupos",
        }

    def clean_username(
            self):
        cpf = self.cleaned_data["username"]
        cpf = User.remover_formatacao(cpf)
        if User.objects.exclude(pk=self.instance.pk).filter(username=cpf).exists():
            raise forms.ValidationError("Um usuário com este CPF já está cadastrado.")
        return cpf


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username", "name", "is_staff", "is_superuser",
            "is_active", "groups"]
        labels = {
            "username": "CPF",
            "name": "Nome Completo",
            "is_staff": "Acessa o sistema?",
            "is_superuser": "É administrador?",
            "is_active": "Está ativo?",
            "groups": "Grupos",
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "000.000.000-00"}),
        }
