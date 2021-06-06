from rest_framework.serializers import (
    ModelSerializer, JSONField
)

from ..models import (
    Eventos,
)


class EventosSerializer(ModelSerializer):
    retorno_envio = JSONField(read_only=True)
    retorno_consulta = JSONField(read_only=True)
    ocorrencias = JSONField(read_only=True)
    class Meta:
        model = Eventos
        fields = '__all__'
        read_only_fields = (
            'status',
            'transmissor_evento',
            'validacao_precedencia',
            'validacoes',
            'arquivo_original',
            'arquivo',
            'transmissor_evento_error',
            'retorno_envio',
            'retorno_envio_json',
            'retorno_consulta',
            'retorno_consulta_json',
            'ocorrencias',
            'ocorrencias_json',
        )
