from rest_framework.serializers import (
    ModelSerializer, JSONField, IntegerField, BooleanField
)

from ..models import (
    Eventos,
)


class EventosSerializer(ModelSerializer):
    from ..choices import EVENTO_ORIGEM_API
    retorno_envio = JSONField(read_only=True)
    retorno_consulta = JSONField(read_only=True)
    ocorrencias = JSONField(read_only=True)
    is_aberto = BooleanField(default=False, initial=False, read_only=True)
    origem = IntegerField(default=EVENTO_ORIGEM_API, initial=EVENTO_ORIGEM_API, read_only=True)
    class Meta:
        model = Eventos
        fields = '__all__'
        read_only_fields = (
            'tpamb',
            'procemi',
            'status',
            'transmissor_evento',
            'validacao_precedencia',
            'validacoes',
            'arquivo',
            'origem',
            'is_aberto',
            'transmissor_evento_error',
            'retorno_envio',
            'retorno_envio_json',
            'retorno_consulta',
            'retorno_consulta_json',
            'ocorrencias',
            'ocorrencias_json',
            'created_by',
        )
