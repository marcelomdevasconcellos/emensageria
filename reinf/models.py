import jsonfield
from django.apps import apps
from django.db import models
from django.db.models import Count, Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import ModelSerializer
from django.contrib.postgres.fields import JSONField

from config.mixins import BaseModelReinf, BaseModelSerializer

from .choices import (
    CHOICES_INSCRICOESTIPOS,
    CHOICES_PROCEMI,
    CHOICES_TPAMB,
    TPINSC_TRANSMISSOR_EVENTOS,
    TIPO_TRANSMISSOR_EVENTOS,
    CODIGO_RESPOSTA,
    CODIGO_STATUS_EFDREINF,
    EVENTOS_GRUPOS,
    IMPORTACAO_STATUS,
    SIM_NAO,
    TIPO_INSCRICAO,
    TRANSMISSOR_STATUS,
    VERSOES,
    EVENTO_STATUS,
    OPERACOES,
    EVENTOS,
    STATUS_EVENTO_CADASTRADO,
    STATUS_EVENTO_AGUARD_ENVIO,
    ARQUIVOS_TIPOS,
    SERVICOS,
)

get_model = apps.get_model


class Arquivos(BaseModelReinf):
    arquivo = models.CharField(max_length=300, )
    data_criacao = models.DateField()
    permite_recuperacao = models.IntegerField(choices=SIM_NAO, )

    class Meta:
        verbose_name = 'Arquivos'
        verbose_name_plural = 'Arquivos'


class ArquivosSerializer(BaseModelSerializer):
    class Meta:
        model = Arquivos


class ImportacaoArquivos(BaseModelReinf):
    arquivo = models.CharField(max_length=200, blank=True, )
    status = models.IntegerField(choices=IMPORTACAO_STATUS, blank=True, )
    data_hora = models.DateTimeField(blank=True, )
    quant_total = models.IntegerField(blank=True, null=True, )
    quant_aguardando = models.IntegerField(blank=True, null=True, )
    quant_processado = models.IntegerField(blank=True, null=True, )
    quant_importado = models.IntegerField(blank=True, null=True, )
    quant_erros = models.IntegerField(blank=True, null=True, )

    class Meta:
        verbose_name = 'Importação de Arquivos'
        verbose_name_plural = 'Importação de Arquivos'
        ordering = [
            'arquivo', ]


class ImportacaoArquivosSerializer(BaseModelSerializer):
    class Meta:
        model = ImportacaoArquivos


class ImportacaoArquivosEventos(BaseModelReinf):
    importacao_arquivos = models.ForeignKey(
        'ImportacaoArquivos',
        on_delete=models.PROTECT,
        related_name='%(class)s_importacao_arquivos',
        blank=True, )
    arquivo = models.CharField(max_length=200, blank=True, null=True, )
    evento = models.CharField(max_length=100, blank=True, null=True, )
    versao = models.CharField(max_length=30, blank=True, null=True, )
    identidade_evento = models.CharField(
        max_length=100, blank=True, null=True, )
    identidade = models.IntegerField(blank=True, null=True, )
    status = models.IntegerField(
        choices=IMPORTACAO_STATUS, blank=True, null=True, )
    data_hora = models.DateTimeField(blank=True, null=True, )
    validacoes = models.TextField(blank=True, null=True, )

    class Meta:
        verbose_name = 'Eventos de Arquivos Importados'
        verbose_name_plural = 'Eventos de Arquivos Importados'
        ordering = [
            'importacao_arquivos',
            'arquivo',
            'evento',
            'versao',
            'identidade_evento',
            'identidade', ]


class ImportacaoArquivosEventosSerializer(BaseModelSerializer):
    class Meta:
        model = ImportacaoArquivosEventos


class Relatorios(BaseModelReinf):
    titulo = models.CharField(max_length=500, )
    campos = models.CharField(max_length=500, )
    sql = models.TextField(blank=True, null=True, )

    class Meta:
        verbose_name = 'Relatórios'
        verbose_name_plural = 'Relatórios'


class RelatoriosSerializer(BaseModelSerializer):
    class Meta:
        model = Relatorios


class Transmissor(BaseModelReinf):
    transmissor_tpinsc = models.IntegerField(choices=TIPO_INSCRICAO, )
    transmissor_nrinsc = models.CharField(max_length=15)
    nome_empresa = models.CharField(max_length=200, unique=True)
    logotipo = models.FileField(upload_to="logotipo",
                                blank=True, null=True, )
    endereco_completo = models.TextField(null=True,)
    nrinsc = models.CharField(max_length=15, unique=True)
    tpinsc = models.IntegerField(choices=TIPO_INSCRICAO, )
    certificado = models.ForeignKey(
        'Certificados',
        on_delete=models.PROTECT,
        related_name='%(class)s_certificado',)

    def __str__(self):
        return self.nome_empresa

    def save(self, **kwargs):
        from .functions import retirar_pontuacao_cpf_cnpj
        self.transmissor_nrinsc = retirar_pontuacao_cpf_cnpj(
            self.transmissor_nrinsc)
        self.nrinsc = retirar_pontuacao_cpf_cnpj(self.nrinsc)
        super(Transmissor, self).save(**kwargs)

    class Meta:
        verbose_name = 'Transmissor'
        verbose_name_plural = 'Transmissor'


class TransmissorSerializer(BaseModelSerializer):
    class Meta:
        model = Transmissor


class TransmissorEventos(BaseModelReinf):
    transmissor = models.ForeignKey(
        'Transmissor',
        on_delete=models.PROTECT,
        related_name='%(class)s_transmissor',
        blank=True, null=True, )
    empregador_tpinsc = models.IntegerField(choices=TIPO_INSCRICAO, )
    empregador_nrinsc = models.CharField(max_length=15, )
    grupo = models.IntegerField(choices=EVENTOS_GRUPOS, )
    status = models.IntegerField(
        choices=TRANSMISSOR_STATUS, blank=True, default=0, )
    resposta_codigo = models.IntegerField(
        choices=CODIGO_RESPOSTA, blank=True, null=True, )
    resposta_descricao = models.TextField(blank=True, null=True, )
    recepcao_data_hora = models.DateTimeField(blank=True, null=True, )
    recepcao_versao_aplicativo = models.CharField(
        max_length=50, blank=True, null=True, )
    protocolo = models.CharField(max_length=50, blank=True, null=True, )
    processamento_versao_aplicativo = models.CharField(
        max_length=50, blank=True, null=True, )
    tempo_estimado_conclusao = models.IntegerField(blank=True, null=True, )
    arquivo_header = models.CharField(max_length=200, blank=True, null=True, )
    arquivo_request = models.CharField(max_length=200, blank=True, null=True, )
    arquivo_response = models.CharField(
        max_length=200, blank=True, null=True, )
    data_hora_envio = models.DateTimeField(blank=True, null=True, )
    data_hora_consulta = models.DateTimeField(blank=True, null=True, )
    retorno_envio_json = models.TextField(
        "retorno_envio_json", blank=True, null=True)
    retorno_consulta_json = models.TextField(
        "retorno_consulta_json", blank=True, null=True)
    ocorrencias_json = models.TextField(
        "ocorrencias_json", blank=True, null=True)

    def quant_eventos(self):
        return Eventos.objects. \
                filter(transmissor_evento_id=transmissor_id,
                    status=STATUS_EVENTO_AGUARD_ENVIO).count()

    def eventos(self):
        from .choices import STATUS_EVENTO_AGUARD_ENVIO
        evts_txt = ''
        evts = Eventos.objects.filter(
            transmissor_evento=self.id,
            status=STATUS_EVENTO_AGUARD_ENVIO).all()
        for evt in evts:
            evts_txt += '<evento Id="{}">{}</evento>'.format(
                evt.identidade,
                str(evt.evento_xml) )
        return evts_txt

    def make_send(self):
        base = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                        xmlns:v1="http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/v1_1_0">
            <soapenv:Header/>
            <soapenv:Body>
                <v1:EnviarLoteEventos><!--Optional:-->
                    <v1:loteEventos>
                        <eSocial xmlns="http://www.esocial.gov.br/schema/lote/eventos/envio/v1_1_1">
                            <envioLoteEventos grupo="{}">
                                <ideEmpregador>
                                    <tpInsc>{}</tpInsc>
                                    <nrInsc>{}</nrInsc>
                                </ideEmpregador>
                                <ideTransmissor>
                                    <tpInsc>{}</tpInsc>
                                    <nrInsc>{}</nrInsc>
                                </ideTransmissor>
                                <eventos>{}</eventos>
                            </envioLoteEventos>
                        </eSocial>
                    </v1:loteEventos>
                </v1:EnviarLoteEventos>
            </soapenv:Body>
        </soapenv:Envelope>"""
        while ' <' in base: base=base.replace('\n', '').replace(' <', '<').replace('  ', ' ')
        return base.format(
            self.grupo, 
            self.empregador_tpinsc, 
            self.empregador_nrinsc,
            self.transmissor.transmissor_tpinsc, 
            self.transmissor.transmissor_nrinsc, 
            str(self.eventos()))

    def make_retrieve(self):
        base = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                          xmlns:v1="http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/consulta/retornoProcessamento/v1_1_0">
            <soapenv:Header/>
            <soapenv:Body>
                <v1:ConsultarLoteEventos>
                    <v1:consulta>
                        <eSocial xmlns="http://www.esocial.gov.br/schema/lote/eventos/envio/consulta/retornoProcessamento/v1_0_0"
                                 xmlns:xs="http://www.w3.org/2001/XMLSchema">
                            <consultaLoteEventos>
                                <protocoloEnvio>{}</protocoloEnvio>
                            </consultaLoteEventos>
                        </eSocial>
                    </v1:consulta>
                </v1:ConsultarLoteEventos>
            </soapenv:Body>
        </soapenv:Envelope>"""
        while ' <' in base: base=base.replace('\n', '').replace(' <', '<').replace('  ', ' ')
        return base.format(
            self.protocolo)

    class Meta:
        verbose_name = 'Transmissor do eSocial'
        verbose_name_plural = 'Transmissor do eSocial'


class TransmissorEventosSerializer(BaseModelSerializer):
    class Meta:
        model = TransmissorEventos


class TransmissorEventosArquivos(BaseModelReinf):

    transmissor_evento = models.ForeignKey(
        'TransmissorEventos',
        on_delete=models.PROTECT,
        related_name='%(class)s_transmissor_evento',
        blank=True, null=True, )
    servico = models.IntegerField('Serviço', choices=SERVICOS,)
    tipo = models.IntegerField('Tipo', choices=ARQUIVOS_TIPOS, )
    arquivo = models.CharField('Nome do arquivo', max_length=200,)
    conteudo = models.TextField('Conteúdo do arquivo',)
    class Meta:
        verbose_name = 'Arquivo do transmissor do eSocial'
        verbose_name_plural = 'Arquivos do transmissor do eSocial'


class Certificados(BaseModelReinf):
    from django.core.files.storage import FileSystemStorage
    from config.settings import BASE_DIR
    from constance import config

    nome = models.CharField(max_length=300, )
    fs_certificado = FileSystemStorage(location=BASE_DIR + config.CERT_PATH)
    certificado = models.FileField(storage=fs_certificado)
    senha = models.CharField(max_length=300, blank=True, null=True, )

    def cert_pem_file(self):
        return '%s%scert_%s.pem' % (self.BASE_DIR, self.config.CERT_PATH, self.id)

    def key_pem_file(self):
        return '%s%skey_%s.pem' % (self.BASE_DIR, self.config.CERT_PATH, self.id)

    def cert_host(self):
        return '%s%s%s' % (self.BASE_DIR, self.config.CERT_PATH, self.certificado)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Certificados'
        verbose_name_plural = 'Certificados'
        ordering = [
            'nome', ]


class CertificadosSerializer(BaseModelSerializer):
    class Meta:
        model = Certificados


class Eventos(BaseModelReinf):
    from config.settings import VERSAO_LAYOUT_REINF

    identidade = models.CharField('Identidade', 
        max_length=36,
        blank=True,
        null=True, )
    versao = models.CharField('Versão', 
        choices=VERSOES,
        max_length=20, 
        default=VERSAO_LAYOUT_REINF, )
    evento = models.CharField('Evento', 
        choices=EVENTOS,
        max_length=20, 
        default='v1_04_00', )
    operacao = models.IntegerField(
        'Operações', 
        choices=OPERACOES, 
        blank=True, null=True, )
    status = models.IntegerField(
        'Status', 
        choices=EVENTO_STATUS, 
        blank=True, 
        default=STATUS_EVENTO_CADASTRADO, )
    tpinsc = models.IntegerField(
        'Tipo de inscrição',
        choices=CHOICES_INSCRICOESTIPOS)
    nrinsc = models.CharField(
        'Numero de inscrição', 
        max_length=15, )
    tpamb = models.IntegerField(
        'Identificação do ambiente', 
        choices=CHOICES_TPAMB, null=True, )
    procemi = models.IntegerField(
        'Processo de emissão do evento',
        choices=CHOICES_PROCEMI, null=True, default=1, )
    verproc = models.CharField(
        'Versão do processo',
        max_length=20, null=True, )
    
    

    #####

    transmissor_evento = models.ForeignKey(
        'TransmissorEventos',
        on_delete=models.PROTECT,
        related_name='%(class)s_transmissor_evento',
        blank=True, null=True, )

    validacao_precedencia = models.IntegerField(
        choices=SIM_NAO, blank=True, null=True, )
    validacoes = models.TextField(blank=True, null=True, )

    arquivo_original = models.IntegerField(
        choices=SIM_NAO, blank=True, null=True, default=0, )
    arquivo = models.CharField(max_length=200, blank=True, null=True, )

    transmissor_evento_error = models.ManyToManyField(
        'TransmissorEventos',
        related_name='%(class)s_transmissor_eventos_erros',
        blank=True, )

    retorno_envio_json = models.TextField(
        "retorno_envio_json", default='{}', blank=True)
    retorno_consulta_json = models.TextField(
        "retorno_consulta_json", default='{}', blank=True)
    evento_json = models.TextField("JSON", default='{}', blank=True)
    evento_xml = models.TextField("XML", null=True, blank=True)
    ocorrencias_json = models.TextField("ocorrencias_json", default='{}', blank=True)

    def __str__(self):
        return self.identidade

    def create_xml(self):
        from json2xml import json2xml
        from json2xml.utils import readfromstring
        import xml.etree.ElementTree as ET
        from .functions import assinar
        from .choices import EVENTO_COD

        data = readfromstring(self.evento_json)
        xml = json2xml.Json2xml(data, 
                wrapper="Reinf", pretty=False, 
                attr_type=False).to_xml()
    
        ET.register_namespace("", "http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/v02_05_00")
        xml_obj = ET.fromstring(xml)

        def recursive_remove(elem2):
            for elem in elem2:
                if len(elem) == 0 and (elem.text is None or not elem.text.strip() ):
                    elem2.remove(elem)
                else:
                    recursive_remove(elem)

        def get_empty_tags():
            empty_tags = []
            for el in xml_obj.iter():
                if len(el) == 0 and (el.text is None or not el.text.strip() ):
                    empty_tags.append(el)
            return empty_tags

        while get_empty_tags():
            for elem in xml_obj:
                recursive_remove(elem)

        xml_obj.set('Id', self.identidade)
        xml_obj.find(EVENTO_COD[self.evento]['codigo']).set('Id', self.identidade)
        xml_obj = assinar(self, xml_obj)

        evento_xml = ET.tostring(xml_obj)
        Eventos.objects.filter(id=self.id).update(evento_xml=evento_xml.decode("utf-8"))


    def save(self, 
            force_insert=False, 
            force_update=False, 
            using=None,
            update_fields=None):
        super(Eventos, self).save(
            force_insert=False, 
            force_update=False, 
            using=None,
            update_fields=None)
        if not self.identidade:
            from .functions import identidade_evento
            Eventos.objects.filter(id=self.id).\
                update(identidade=identidade_evento(self))

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = [
            'versao',
            'evento',
            'operacao',
            'status',]



class EventosSerializer(BaseModelSerializer):

    class Meta:

        model = Eventos
        fields = '__all__'
        read_only_fields = (
            # 'identidade',
            # 'versao',
            # 'evento',
            # 'operacao',
            # 'tpinsc',
            # 'nrinsc',
            # 'tpamb',
            # 'procemi',
            # 'verproc',
            # 'evento_json',
            'status',
            'transmissor_evento',
            'validacao_precedencia',
            'validacoes',
            'arquivo_original',
            'arquivo',
            'transmissor_evento_error',
            'retorno_envio_json',
            'retorno_consulta_json',
            'ocorrencias_json',
        )

