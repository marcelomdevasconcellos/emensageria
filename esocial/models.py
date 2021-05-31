from django.apps import apps
from django.db import models

from config.mixins import BaseModelEsocial, BaseModelSerializer
from .choices import (
    CHOICES_INSCRICOESTIPOS,
    CHOICES_PROCEMI,
    CHOICES_TPAMB,
    CODIGO_RESPOSTA,
    EVENTOS_GRUPOS,
    ARQUIVO_FONTE,
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
from django.core.files.storage import FileSystemStorage
from config.settings import BASE_DIR
from constance import config


get_model = apps.get_model


class Arquivos(BaseModelEsocial):
    cols = {
        'arquivo': 12,
        'created_at': 3,
        'created_by': 3,
        'updated_at': 3,
        'updated_by': 3,
    }
    fs_arquivo = FileSystemStorage(
        location=BASE_DIR + '/arquivos/eventos/esocial')
    arquivo = models.FileField(
        'Arquivo', storage=fs_arquivo)
    permite_recuperacao = models.IntegerField(
        'Permite recuperação',
        choices=SIM_NAO,
        default=1)
    fonte = models.IntegerField(
        'Fonte',
        choices=ARQUIVO_FONTE,
        default=1)
    evento = models.ManyToManyField(
        'Eventos',
        verbose_name='Evento',
        related_name='%(class)s_evento',
        blank=True, )

    def __str__(self):
        return self.arquivo.name

    class Meta:
        verbose_name = 'Arquivo'
        verbose_name_plural = 'Arquivos'


class ArquivosSerializer(BaseModelSerializer):
    class Meta:
        model = Arquivos


class Relatorios(BaseModelEsocial):
    cols = {
        'titulo': 12,
        'campos': 12,
        'sql': 12,
        'created_at': 3,
        'created_by': 3,
        'updated_at': 3,
        'updated_by': 3,
    }
    titulo = models.CharField('Título', max_length=500, )
    campos = models.CharField('Campos',
                              help_text='Inclua os campos separando eles por ponto e vírgula', max_length=500, )
    sql = models.TextField('Comando SQL', blank=True, null=True, )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Relatórios'
        verbose_name_plural = 'Relatórios'


class RelatoriosSerializer(BaseModelSerializer):
    class Meta:
        model = Relatorios


class Transmissor(BaseModelEsocial):
    cols = {
        'transmissor_tpinsc': 6,
        'transmissor_nrinsc': 6,
        'nome_empresa': 6,
        'logotipo': 6,
        'endereco_completo': 12,
        'nrinsc': 6,
        'tpinsc': 6,
        'certificado': 12,
        'created_at': 3,
        'created_by': 3,
        'updated_at': 3,
        'updated_by': 3,
    }
    transmissor_tpinsc = models.IntegerField(
        'Tipo de inscrição do transmissor', choices=TIPO_INSCRICAO, )
    transmissor_nrinsc = models.CharField(
        'Número de inscrição do transmissor', max_length=15)
    nome_empresa = models.CharField(
        'Nome da empresa', max_length=200, unique=True)
    logotipo = models.FileField(
        'Logotipo', upload_to="logotipo",
        blank=True, null=True )
    endereco_completo = models.TextField(
        'Endereço', null=True, blank=True )
    tpinsc = models.IntegerField(
        'Tipo de inscrição', choices=TIPO_INSCRICAO, )
    nrinsc = models.CharField(
        'Número de inscrição', max_length=15, unique=True)
    certificado = models.ForeignKey(
        'Certificados',
        on_delete=models.PROTECT,
        verbose_name='Certificado',
        related_name='%(class)s_certificado', )

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


class TransmissorEventos(BaseModelEsocial):
    cols = {
        'transmissor': 12,
        'arquivo_header': 12,
        'arquivo_request': 12,
        'arquivo_response': 12,
        'retorno_envio_json': 12,
        'retorno_consulta_json': 12,
        'ocorrencias_json': 12,
        'created_at': 3,
        'created_by': 3,
        'updated_at': 3,
        'updated_by': 3,
    }
    transmissor = models.ForeignKey(
        'Transmissor',
        on_delete=models.PROTECT,
        verbose_name='Transmissor',
        related_name='%(class)s_transmissor',
        blank=True, null=True, )
    empregador_tpinsc = models.IntegerField('Tipo de inscrição do empregador', choices=TIPO_INSCRICAO, )
    empregador_nrinsc = models.CharField('Número de inscrição do empregador', max_length=15, )
    grupo = models.IntegerField('Grupo', choices=EVENTOS_GRUPOS, )
    status = models.IntegerField(
        'Status',
        choices=TRANSMISSOR_STATUS, blank=True, default=0, )
    resposta_codigo = models.CharField(
        'Código da Resposta', max_length=10, blank=True, null=True, )
    resposta_descricao = models.TextField('Descrição da resposta', blank=True, null=True, )
    data_hora_envio = models.DateTimeField('Data/Hora do envio', blank=True, null=True, )
    data_hora_consulta = models.DateTimeField('Data/Hora da consulta', blank=True, null=True, )
    recepcao_data_hora = models.DateTimeField('Data/Hora da recepção', blank=True, null=True, )
    recepcao_versao_aplicativo = models.CharField(
        'Versão do aplicativo de recepção',
        max_length=50, blank=True, null=True, )
    protocolo = models.CharField('Protocolo', max_length=50, blank=True, null=True, )
    processamento_versao_aplicativo = models.CharField(
        'Versão do aplicativo de processamento', max_length=50, blank=True, null=True, )
    tempo_estimado_conclusao = models.IntegerField('Tempo estimado de conclusão', blank=True, null=True, )
    arquivo_header = models.CharField('Arquivo header', max_length=200, blank=True, null=True, )
    arquivo_request = models.CharField('Arquivo request', max_length=200, blank=True, null=True, )
    arquivo_response = models.CharField(
        'Arquivo response', max_length=200, blank=True, null=True, )
    retorno_envio_json = models.TextField(
        "Retorno do envio", blank=True, null=True)
    retorno_consulta_json = models.TextField(
        "Retorno da consulta", blank=True, null=True)
    ocorrencias_json = models.TextField(
        "Ocorrências", blank=True, null=True)

    def quant_eventos(self):
        return Eventos.objects. \
            filter(transmissor_evento_id=self.id,
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
                str(evt.evento_xml))
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
        while ' <' in base: base = base.replace('\n', '').replace(' <', '<').replace('  ', ' ')
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
        while ' <' in base: base = base.replace('\n', '').replace(' <', '<').replace('  ', ' ')
        return base.format(
            self.protocolo)

    def __str__(self):
        return '{} {} {}'.format(self.id, self.grupo, self.get_status_display())

    class Meta:
        verbose_name = 'Transmissor do eSocial'
        verbose_name_plural = 'Transmissor do eSocial'


class TransmissorEventosSerializer(BaseModelSerializer):
    class Meta:
        model = TransmissorEventos


class TransmissorEventosArquivos(BaseModelEsocial):
    transmissor_evento = models.ForeignKey(
        'TransmissorEventos',
        on_delete=models.CASCADE,
        related_name='%(class)s_transmissor_evento',
        blank=True, null=True, )
    servico = models.IntegerField('Serviço', choices=SERVICOS, )
    tipo = models.IntegerField('Tipo', choices=ARQUIVOS_TIPOS, )
    arquivo = models.CharField('Nome do arquivo', max_length=200, )
    conteudo = models.TextField('Conteúdo do arquivo', )

    def __str__(self):
        return '{} {} {}'.format(self.transmissor_evento, self.get_servico_display(), self.get_tipo_display())

    class Meta:
        verbose_name = 'Arquivo'
        verbose_name_plural = 'Arquivos'


class Certificados(BaseModelEsocial):
    cols = {
        'nome': 12,
        'certificado': 12,
        'senha': 12,
        'created_at': 3,
        'created_by': 3,
        'updated_at': 3,
        'updated_by': 3,
    }
    nome = models.CharField('Nome', max_length=300, )
    fs_certificado = FileSystemStorage(location=BASE_DIR + config.CERT_PATH)
    certificado = models.FileField('Arquivo', storage=fs_certificado)
    senha = models.CharField('Senha',  max_length=300, blank=True, null=True, )

    def cert_pem_file(self):
        return '%s%scert_%s.pem' % (BASE_DIR, config.CERT_PATH, self.id)

    def key_pem_file(self):
        return '%s%skey_%s.pem' % (BASE_DIR, config.CERT_PATH, self.id)

    def cert_host(self):
        return '%s%s%s' % (BASE_DIR, config.CERT_PATH, self.certificado)

    def capath(self):
        return '%s%sesocial' % (BASE_DIR, config.CERT_PATH)

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


class Eventos(BaseModelEsocial):
    from config.settings import VERSAO_LAYOUT_ESOCIAL
    from .choices import ESOCIAL_VERSAO_DEFAULT
    cols = {
        'evento': 8,
        'evento_json': 12,
    }
    identidade = models.CharField('Identidade',
                                  max_length=36,
                                  blank=True,
                                  null=True, )
    versao = models.CharField('Versão',
                              choices=VERSOES,
                              max_length=20,
                              default=ESOCIAL_VERSAO_DEFAULT, )
    evento = models.CharField('Evento',
                              choices=EVENTOS,
                              max_length=20, )
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
        verbose_name='Transmissor',
        related_name='%(class)s_transmissor_evento',
        blank=True, null=True, )

    validacao_precedencia = models.IntegerField(
        'Validação de precedência',
        choices=SIM_NAO, blank=True, null=True, )

    validacoes = models.TextField(
        'Validações', blank=True, null=True, )

    arquivo = models.CharField(
        'Arquivo', max_length=200, blank=True, null=True, )

    arquivo = models.ManyToManyField(
        'Arquivos',
        verbose_name='Arquivo',
        related_name='%(class)s_arquivo',
        blank=True, )

    transmissor_evento_error = models.ManyToManyField(
        'TransmissorEventos',
        verbose_name='Transmissores (Erro)',
        related_name='%(class)s_transmissor_eventos_erros',
        blank=True, )

    retorno_envio_json = models.TextField(
        'Retorno do envio',
        "retorno_envio_json", default='{}', blank=True)
    retorno_consulta_json = models.TextField(
        'Retorno da consulta',
        "retorno_consulta_json", default='{}', blank=True)
    evento_json = models.TextField("JSON", default='{}', blank=True)
    evento_xml = models.TextField("XML", null=True, blank=True)
    ocorrencias_json = models.TextField("Ocorrências", default='{}', blank=True)

    def __str__(self):
        return self.identidade

    def autorizar_envio_evento(self):
        from datetime import datetime
        from .models import Eventos, Transmissor, TransmissorEventos
        from .choices import (
            STATUS_EVENTO_CADASTRADO,
            STATUS_EVENTO_AGUARD_ENVIO,
            STATUS_TRANSMISSOR_CADASTRADO,
            EVENTOS_GRUPOS_TABELAS, )

        transmissor = Transmissor.objects. \
            filter(nrinsc=self.nrinsc).all()

        if transmissor:
            transmissor = transmissor[0]
            tevt = TransmissorEventos.objects.filter(
                empregador_tpinsc=transmissor.tpinsc,
                empregador_nrinsc=transmissor.nrinsc,
                grupo=EVENTOS_GRUPOS_TABELAS,
                status=STATUS_TRANSMISSOR_CADASTRADO).all()
            if tevt:
                tevt = tevt[0]
            else:
                tevt_data = {
                    'transmissor': transmissor,
                    'empregador_tpinsc': transmissor.tpinsc,
                    'empregador_nrinsc': transmissor.nrinsc,
                    'grupo': EVENTOS_GRUPOS_TABELAS,
                    'status': STATUS_TRANSMISSOR_CADASTRADO,
                }
                tevt = TransmissorEventos(**tevt_data)
                tevt.save()
            Eventos.objects.filter(
                id=self.id).update(
                transmissor_evento_id=tevt.id,
                status=STATUS_EVENTO_AGUARD_ENVIO)
            return (0, 'Evento vinculado com sucesso ao transmissor!')
        else:
            return (1, '''Erro ao vincular evento. Não foi encontrato 
                nenhum transmissor com o número de inscrição: 
                %s !''' % self.nrinsc)

    def create_xml(self):
        from json2xml import json2xml
        from json2xml.utils import readfromstring
        import xml.etree.ElementTree as ET
        from .functions import assinar
        from .choices import EVENTO_COD

        data = readfromstring(self.evento_json)
        xml = json2xml.Json2xml(data,
                                wrapper="eSocial", pretty=False,
                                attr_type=False).to_xml()
        ET.register_namespace("", f"http://www.esocial.gov.br/schema/evt/evtInfoEmpregador/{self.versao}")
        xml_obj = ET.fromstring(xml)

        def recursive_remove(elem2):
            for elem in elem2:
                if len(elem) == 0 and (elem.text is None or not elem.text.strip()):
                    elem2.remove(elem)
                else:
                    recursive_remove(elem)

        def get_empty_tags():
            empty_tags = []
            for el in xml_obj.iter():
                if len(el) == 0 and (el.text is None or not el.text.strip()):
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
            Eventos.objects.filter(id=self.id). \
                update(identidade=identidade_evento(self))

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = [
            'versao',
            'evento',
            'operacao',
            'status', ]


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
