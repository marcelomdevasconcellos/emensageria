from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from .forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    # Usa os formulários personalizados para criação e edição
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    # Configuração dos campos para visualização e edição no admin
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informações pessoais", {"fields": ("name", "first_name", "last_name")}),
        ("Permissões",
         {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
        ("Informações adicionais", {"fields": ("eventos",)}),
    )
    list_display = [
        "username",
        "name",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_superuser"
    ]
    search_fields = (
        "username",
        "name",
        "user_search_str",
        "first_name",
        "last_name",
    )
