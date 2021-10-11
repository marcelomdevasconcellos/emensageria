import xmltodict
from rest_framework.serializers import (
    ModelSerializer,
    JSONField,
    IntegerField,
    BooleanField,
    ChoiceField,
    CharField,
)

from ..models import (
    Eventos, TransmissorEventos
)

from ..choices import EVENTO_ORIGEM_API, EVENTO_ORIGEM, STATUS_EVENTO_IMPORTADO


class TransmissorEventosSerializer(ModelSerializer):
    class Meta:
        model = TransmissorEventos
        fields = '__all__'


class EventosSerializer(ModelSerializer):
    retorno_envio = JSONField(read_only=True)
    retorno_consulta = JSONField(read_only=True)
    retorno_envio_lote = JSONField(read_only=True)
    retorno_consulta_lote = JSONField(read_only=True)
    ocorrencias = JSONField(read_only=True)
    status_txt = CharField(source='get_status_display', read_only=True)
    tpinsc_txt = CharField(source='get_tpinsc_display', read_only=True)
    tpamb_txt = CharField(source='get_tpamb_display', read_only=True)
    procemi_txt = CharField(source='get_procemi_display', read_only=True)
    origem_txt = CharField(source='get_origem_display', read_only=True)
    transmissor = TransmissorEventosSerializer(source='transmissor_evento', many=False, read_only=True)

    def create(self, validated_data):
        from config.settings import ESOCIAL_TPAMB
        validated_data['origem'] = EVENTO_ORIGEM_API
        validated_data['is_aberto'] = False
        validated_data['status'] = STATUS_EVENTO_IMPORTADO
        validated_data['tpamb'] = ESOCIAL_TPAMB
        if validated_data.get('evento_xml') and not validated_data.get('evento_json'):
            import json
            import xml.etree.ElementTree as ET
            from ..choices import EVENTO_COD
            if not '<eSocial>' in validated_data.get('evento_xml'):
                validated_data['evento_xml'] = '<eSocial>' + validated_data.get('evento_xml') + '</eSocial>'

            evento = validated_data['evento']
            evento_codigo = EVENTO_COD[evento]['codigo']
            versao = validated_data['versao']

            def recursive_update_datefield(elem2):
                from dateutil import parser as dateutil_parser
                for elem in elem2:
                    if elem.text and len(elem.text) == 10 and len(elem.text.split('-')) == 3:
                        data = dateutil_parser.parse(elem.text)
                        elem.text = data.strftime('%d/%m/%Y')
                    else:
                        recursive_update_datefield(elem)

            ET.register_namespace("", f"http://www.esocial.gov.br/schema/evt/{evento_codigo}/{versao}")
            xml_obj = ET.fromstring(validated_data['evento_xml'])
            for elem in xml_obj:
                recursive_update_datefield(elem)
            xml_string = ET.tostring(xml_obj)
            dict = xmltodict.parse(xml_string)
            validated_data['evento_json'] = json.dumps(dict.get('eSocial'))

        return super().create(validated_data)

    def update(self, instance, validated_data):
        from config.settings import ESOCIAL_TPAMB
        validated_data['origem'] = EVENTO_ORIGEM_API
        validated_data['is_aberto'] = False
        validated_data['status'] = STATUS_EVENTO_IMPORTADO
        validated_data['ocorrencias_json'] = None
        validated_data['tpamb'] = ESOCIAL_TPAMB
        validated_data['retorno_envio_json'] = '{}'
        validated_data['retorno_consulta_json'] = '{}'
        if validated_data['evento_xml'] and not validated_data['evento_json']:
            import json
            import xml.etree.ElementTree as ET
            from ..choices import EVENTO_COD
            if not '<eSocial>' in validated_data.get('evento_xml'):
                validated_data['evento_xml'] = '<eSocial>' + validated_data.get('evento_xml') + '</eSocial>'

            evento = validated_data['evento']
            evento_codigo = EVENTO_COD[evento]['codigo']
            versao = validated_data['versao']

            def recursive_update_datefield(elem2):
                from dateutil import parser as dateutil_parser
                for elem in elem2:
                    if elem.text and len(elem.text) == 10 and len(elem.text.split('-')) == 3:
                        data = dateutil_parser.parse(elem.text)
                        elem.text = data.strftime('%d/%m/%Y')
                    else:
                        recursive_update_datefield(elem)

            ET.register_namespace("", f"http://www.esocial.gov.br/schema/evt/{evento_codigo}/{versao}")
            xml_obj = ET.fromstring(validated_data['evento_xml'])
            for elem in xml_obj:
                recursive_update_datefield(elem)
            xml_string = ET.tostring(xml_obj)
            dict = xmltodict.parse(xml_string)
            validated_data['evento_json'] = json.dumps(dict.get('eSocial'))
        return super().update(instance, validated_data)

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
            'is_aberto',
            'origem',
            'transmissor_evento_error',
            'retorno_envio',
            'retorno_envio_json',
            'retorno_envio_lote_json',
            'retorno_consulta',
            'retorno_consulta_json',
            'retorno_consulta_lote_json',
            'ocorrencias',
            'ocorrencias_json',
            'created_by',
        )
