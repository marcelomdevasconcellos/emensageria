import re

import unicodedata
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from apps.esocial.choices import EVENTOS
from multiselectfield import MultiSelectField


def remover_acentos_caracteres_especiais(
        palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub(r'[^a-zA-Z0-9 ]', '', palavraSemAcento)


class User(AbstractUser):
    cols = {
        'name': 4,
        'eventos': 12,
    }
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'CPF',
        max_length=14,
        unique=True,
        help_text='Obrigatório. Informe o CPF do usuário.',
        validators=[username_validator],
        error_messages={
            'unique': "Um usuário com este CPF já está cadastrado no sistema.",
        },
    )

    name = CharField("Nome Completo", blank=True, max_length=255)

    eventos = MultiSelectField(
        "Eventos", choices=EVENTOS, null=True, blank=True)

    # def get_eventos_keys(self):
    #     print(self.eventos)
    #     # Retorna a lista de eventos selecionados como uma lista de valores
    #     return self.eventos

    is_staff = models.BooleanField(
        "Acessa o sistema?",
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        "Está ativo?",
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    is_superuser = models.BooleanField(
        "É administrador?",
        default=False,
        help_text=(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name="Grupos",
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )

    user_str = models.CharField(
        'User String',
        blank=True, null=True, max_length=200, )

    user_search_str = models.CharField(
        'User Search String',
        blank=True, null=True, max_length=200, )

    @staticmethod
    def formatar_cpf(
            cpf):
        return f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"

    @staticmethod
    def remover_formatacao(
            cpf):
        return cpf.replace('.', '').replace('-', '')

    def remover_formatacao_cpf(
            self):
        if self.username:
            return self.username.replace('.', '').replace('-', '')
        return ""

    def get_cpf_formatado(
            self):
        if self.username:
            cpf = self.username
            cpf = cpf.replace('.', '').replace('-', '')
        return self.formatar_cpf(cpf)

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None):
        username = self.username
        username = self.remover_formatacao(username)
        username = self.formatar_cpf(username)
        self.username = username
        if self.name:
            if ' ' in self.name:
                name = self.name.split(' ')
            else:
                name = [self.name, self.name]
            if not self.first_name:
                self.first_name = name[0]
            if not self.last_name:
                self.last_name = name[-1]
        if self.pk:
            self.user_str = '{:08n} {} {} ({})'.format(
                self.pk, self.first_name or "",
                self.last_name or "", self.username or "")
            self.user_search_str = '{} {}'.format(
                self.remover_formatacao_cpf(),
                remover_acentos_caracteres_especiais(self.user_str))

        super(User, self).save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
        )
        if not self.user_str:
            self.user_str = '{:08n} {} {} ({})'.format(
                self.pk, self.first_name or "",
                self.last_name or "", self.username or "")
            self.save()

    def get_absolute_url(
            self):
        return reverse("users:detail", kwargs={"username": self.username})

    def nome(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(
            self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.username

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
