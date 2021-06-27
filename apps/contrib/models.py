import jsonfield
from django.apps import apps
from django.db import models
from django.db.models import Count, Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import ModelSerializer
from django.contrib.postgres.fields import JSONField

from config.mixins import BaseModel, BaseModelSerializer

from .choices import *

get_model = apps.get_model


class Leiaute(BaseModel):
    esocial_efdreinf = models.CharField(max_length=10)
    versao = models.CharField(max_length=100)
    evento = models.CharField(max_length=5000)
    evento_codigo = models.CharField(max_length=50)
    evento_slug = models.CharField(max_length=500, blank=True, null=True)
    numero = models.IntegerField()
    numero_esocial = models.IntegerField()
    registro_campo = models.CharField(max_length=100)
    registro_pai = models.CharField(max_length=100, blank=True, null=True)
    elemento = models.CharField(max_length=2)
    tipo = models.CharField(max_length=1, blank=True, null=True)
    ocorrencias = models.CharField(max_length=10)
    tamanho = models.IntegerField(blank=True, null=True)
    casas_decimais = models.IntegerField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    descricao_original = models.TextField(blank=True, null=True)
    validacao = models.TextField(blank=True, null=True)
    valores_validos = models.TextField(blank=True, null=True)

    is_multiplas_ocorrencias = models.BooleanField(default=False)
    ordenacao = models.IntegerField(blank=True, null=True)
    opcoes = models.TextField(blank=True, null=True)
    grupo = models.CharField(max_length=500, blank=True, null=True)
    titulo = models.TextField(max_length=500, blank=True, null=True)
    input_name = models.CharField(max_length=1000, blank=True, null=True)
    input_id = models.CharField(max_length=1000, blank=True, null=True)
    input_value = models.CharField(max_length=1000, blank=True, null=True)
    input_choices_name = models.CharField(max_length=1000, blank=True, null=True)
    input_choices = models.TextField(blank=True, null=True)
    input_html = models.TextField(blank=True, null=True)
    input_html_for = models.TextField(blank=True, null=True)

    modelo_xml = models.ForeignKey(
        'Leiaute',
        on_delete=models.CASCADE,
        related_name='%(class)s_modelo_xml',
        blank=True, null=True)

    modelo_xml_fk = models.ForeignKey(
        'Leiaute',
        on_delete=models.CASCADE,
        related_name='%(class)s_modelo_xml_fk',
        blank=True, null=True)

    class Meta:
        verbose_name = 'Leiaute'
        verbose_name_plural = 'Leiaute'


class Dicionario(BaseModel):
    esocial_efdreinf = models.CharField(max_length=10)
    registro_campo = models.CharField(max_length=100)
    titulo = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = 'Dicionário'
        verbose_name_plural = 'Dicionário'
        unique_together = ('esocial_efdreinf', 'registro_campo')