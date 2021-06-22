import json
import os
import re
from datetime import datetime

import xmltodict
from constance import config
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from config.functions import (create_dir, read_file, save_file)
from config.mixins import BaseModelEsocial, BaseModelSerializer, BaseModel
from .choices import *

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
        location=os.path.join(settings.BASE_DIR, config.FILES_PATH))
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
        'users': 12,
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
        blank=True, null=True)
    endereco_completo = models.TextField(
        'Endereço', null=True, blank=True)
    tpinsc = models.IntegerField(
        'Tipo de inscrição do empregador', choices=TIPO_INSCRICAO,)
    nrinsc = models.CharField(
        'Número de inscrição do empregador', max_length=15, unique=True,
        help_text="O CNPJ completo somente pode ser utilizado por órgãos públicos, " \
                  "os demais empregadores deverão informar somente o CNPJ base (8 primeiros dígitos do CNPJ)")
    certificado = models.ForeignKey(
        'Certificados',
        on_delete=models.PROTECT,
        verbose_name='Certificado',
        related_name='%(class)s_certificado', )
    users = models.ManyToManyField(User, verbose_name='Usuários', related_name='transmissores_users', blank=True,
                                   help_text="Informe a lista de usuários que tem acesso a utilizar este transmissor.")
    def __str__(self):
        return self.nome_empresa

    def save(self, **kwargs):
        self.transmissor_nrinsc = re.sub('[^0-9]', '', self.transmissor_nrinsc)
        self.nrinsc = re.sub('[^0-9]', '', self.nrinsc)
        super(Transmissor, self).save(**kwargs)

    class Meta:
        verbose_name = 'Transmissor'
        verbose_name_plural = 'Transmissor'


class TransmissorSerializer(BaseModelSerializer):
    class Meta:
        model = Transmissor


class TransmissorEventos(BaseModelEsocial):
    cols = {
        'transmissor': 8,
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

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        self.empregador_nrinsc = re.sub('[^0-9]', '', self.empregador_nrinsc)
        super(TransmissorEventos, self).save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None)

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
                read_file(evt.xml_file()))
        return evts_txt

    def make_send(self):
        from .choices import MAKE_SEND
        while ' <' in MAKE_SEND:
            MAKE_SEND = MAKE_SEND.replace('\n', '').replace(' <', '<').replace('  ', ' ')
        return MAKE_SEND.format(
            self.grupo,
            self.empregador_tpinsc,
            self.empregador_nrinsc,
            self.transmissor.transmissor_tpinsc,
            self.transmissor.transmissor_nrinsc,
            str(self.eventos()))

    def make_retrieve(self):
        from .choices import MAKE_RETRIEVE
        while ' <' in MAKE_RETRIEVE:
            MAKE_RETRIEVE = MAKE_RETRIEVE.replace('\n', '').replace(' <', '<').replace('  ', ' ')
        return MAKE_RETRIEVE.format(
            self.protocolo)

    def get_command(self, service, date_now):
        filename = os.path.join(
            settings.BASE_DIR,
            config.FILES_PATH, 'comunicacao',
            service, 'command',
            '{}_{}.txt'.format(
                self.id, datetime.now().strftime('%Y%m%d%H%M%S')))
        create_dir(filename)
        return filename

    def get_header(self, service, date_now):
        filename = os.path.join(
            settings.BASE_DIR,
            config.FILES_PATH, 'comunicacao',
            service, 'header',
            '{}_{}.txt'.format(
                self.id, datetime.now().strftime('%Y%m%d%H%M%S')))
        create_dir(filename)
        return filename

    def get_request(self, service, date_now):
        filename = os.path.join(
            settings.BASE_DIR,
            config.FILES_PATH, 'comunicacao',
            service, 'request',
            '{}_{}.xml'.format(
                self.id, datetime.now().strftime('%Y%m%d%H%M%S')))
        create_dir(filename)
        return filename

    def get_response(self, service, date_now):
        filename = os.path.join(
            settings.BASE_DIR,
            config.FILES_PATH, 'comunicacao',
            service, 'response',
            '{}_{}.xml'.format(
                self.id, datetime.now().strftime('%Y%m%d%H%M%S')))
        create_dir(filename)
        return filename

    def enviar(self, service='WsEnviarLoteEventos', request=None):
        from .choices import COMMAND_CURL
        date_now = datetime.now().strftime('%Y%m%d%H%M%S')

        dados = {'quant_eventos': self.quant_eventos(), 'empregador_tpinsc': self.empregador_tpinsc,
                 'empregador_nrinsc': self.empregador_nrinsc, 'transmissor_tpinsc': self.transmissor.transmissor_tpinsc,
                 'transmissor_nrinsc': self.transmissor.transmissor_nrinsc, 'esocial_lote_min': config.ESOCIAL_LOTE_MIN,
                 'esocial_lote_max': config.ESOCIAL_LOTE_MAX, 'esocial_timeout': int(config.ESOCIAL_TIMEOUT),
                 'transmissor_id': self.id, 'header': self.get_header(service, date_now),
                 'request': self.get_request(service, date_now),
                 'response': self.get_response(service, date_now), 'service': service,
                 'url': URLS_ESOCIAL[config.ESOCIAL_TP_AMB][service]['url'],
                 'action': URLS_ESOCIAL[config.ESOCIAL_TP_AMB][service]['action'],
                 'cert': self.transmissor.certificado.cert_pem_file(),
                 'key': self.transmissor.certificado.key_pem_file(), 'capath': self.transmissor.certificado.capath(),
                 'timeout': int(config.ESOCIAL_TIMEOUT)}

        if self.transmissor.certificado and dados['quant_eventos']:

            if dados['esocial_lote_min'] <= dados['quant_eventos'] <= dados['esocial_lote_max']:

                save_file(dados['request'], self.make_send())
                save_file(self.get_command(service, date_now), COMMAND_CURL % dados)

                os.system(COMMAND_CURL % dados)

                if not os.path.isfile(dados['response']):

                    TransmissorEventos.objects.filter(id=self.id). \
                        update(status=STATUS_TRANSMISSOR_ERRO_ENVIO)

                    if request:
                        messages.error(request, '''Não foi recebida nenhuma resposta do servidor. 
                            Verifique se a pasta /arquivos/ está com permissão de escrita ou 
                            pode ter ocorrido erro de timeout.
                            Timeout atual %(timeout)s''' % dados)
                    return {
                        'status': 'error',
                        'mensagem': '''Não foi recebida nenhuma resposta do servidor. 
                            Verifique se a pasta /arquivos/ está com permissão de escrita ou 
                            pode ter ocorrido erro de timeout.
                            Timeout atual %(timeout)s''' % dados}

                elif 'HTTP/1.1 200 OK' not in read_file(dados['header']):

                    TransmissorEventos.objects.filter(id=self.id). \
                        update(status=STATUS_TRANSMISSOR_ERRO_ENVIO)
                    if request:
                        messages.error(request, 'Retorno do servidor: ' + read_file(dados['header']))

                    return {
                        'status': 'warning',
                        'mensagem': 'Retorno do servidor: ' + read_file(dados['header'])}

                TransmissorEventosArquivos(
                    transmissor_evento=self,
                    arquivo=dados['header'],
                    servico=SERVICO_ENVIAR,
                    tipo=ARQUIVO_TIPO_HEADER,
                    conteudo=read_file(dados['header'])).save()

                TransmissorEventosArquivos(
                    transmissor_evento=self,
                    arquivo=dados['request'],
                    servico=SERVICO_ENVIAR,
                    tipo=ARQUIVO_TIPO_REQUEST,
                    conteudo=read_file(dados['request'])).save()

                TransmissorEventosArquivos(
                    transmissor_evento=self,
                    arquivo=dados['response'],
                    servico=SERVICO_ENVIAR,
                    tipo=ARQUIVO_TIPO_RESPONSE,
                    conteudo=read_file(dados['response'])).save()

                response_dict = xmltodict.parse(read_file(dados['response']))

                response_dict = response_dict["s:Envelope"]["s:Body"]["EnviarLoteEventosResponse"] \
                    ["EnviarLoteEventosResult"]["eSocial"]["retornoEnvioLoteEventos"]

                response_json = json.dumps(response_dict)

                recepcao_data_hora = None
                recepcao_versao_aplicativo = None
                protocolo = None
                ocorrencias_json = json.dumps(response_dict.get("status").get("ocorrencias") or {})
                resposta_codigo = response_dict.get("status").get("cdResposta")
                resposta_descricao = response_dict.get("status").get("descResposta")

                if response_dict.get("dadosRecepcaoLote"):
                    recepcao_data_hora = response_dict.get("dadosRecepcaoLote").get("dhRecepcao")
                    recepcao_versao_aplicativo = response_dict.get("dadosRecepcaoLote").get("versaoAplicativoRecepcao")
                    protocolo = response_dict.get("dadosRecepcaoLote").get("protocoloEnvio")

                self.retorno_envio_json = response_json
                self.resposta_codigo = resposta_codigo
                self.resposta_descricao = resposta_descricao
                self.ocorrencias_json = ocorrencias_json
                self.data_hora_envio = datetime.now()
                self.recepcao_data_hora = recepcao_data_hora
                self.recepcao_versao_aplicativo = recepcao_versao_aplicativo
                self.protocolo = protocolo
                self.arquivo_header = dados['header']
                self.arquivo_request = dados['request']
                self.arquivo_response = dados['response']

                if response_dict["status"]["cdResposta"] not in ('101', '201', '202'):
                    self.status = STATUS_TRANSMISSOR_ERRO_ENVIO
                    self.save()
                    if request:
                        messages.error(request, '{} {}'.format(
                            resposta_codigo,
                            resposta_descricao))
                    return {
                        'status': 'error',
                        'mensagem': '{} {}'.format(
                            resposta_codigo,
                            resposta_descricao)}

                self.status = STATUS_TRANSMISSOR_ENVIADO
                self.save()
                self.transmissor_esocial.update(status=STATUS_EVENTO_ENVIADO)

                if request:
                    messages.success(request, '{} {}'.format(
                        resposta_codigo,
                        resposta_descricao))
                return {
                    'status': 'success',
                    'mensagem': '{} {}'.format(
                        resposta_codigo,
                        resposta_descricao)}

            elif dados['quant_eventos'] < dados['esocial_lote_min']:
                if request:
                    messages.error(request, 'Lote com quantidade inferior a mínima permitida!')
                return {
                    'status': 'error',
                    'mensagem': 'Lote com quantidade inferior a mínima permitida!'}

            elif dados['quant_eventos'] > dados['esocial_lote_max']:
                if request:
                    messages.error(request, 'Lote com quantidade de eventos superior a máxima permitida!')
                return {
                    'status': 'error',
                    'mensagem': 'Lote com quantidade de eventos superior a máxima permitida!'}

            else:
                if request:
                    messages.error(request, 'Ops! Algo aconteceu!')
                return {
                    'status': 'error',
                    'mensagem': 'Ops! Algo aconteceu!'}

        else:
            if request:
                messages.error(request, '''O certificado não está configurado ou não
                                possuem eventos validados para envio neste lote!''')
            return {
                'status': 'error',
                'mensagem': '''O certificado não está configurado ou não
                                possuem eventos validados para envio neste lote!'''}

    def consultar(self, service='WsConsultarLoteEventos', request=None):

        from bs4 import BeautifulSoup
        date_now = datetime.now().strftime('%Y%m%d%H%M%S')
        dados = {'quant_eventos': self.quant_eventos(), 'empregador_tpinsc': self.empregador_tpinsc,
                 'empregador_nrinsc': self.empregador_nrinsc, 'transmissor_tpinsc': self.transmissor.transmissor_tpinsc,
                 'transmissor_nrinsc': self.transmissor.transmissor_nrinsc, 'esocial_lote_min': config.ESOCIAL_LOTE_MIN,
                 'esocial_lote_max': config.ESOCIAL_LOTE_MAX, 'esocial_timeout': int(config.ESOCIAL_TIMEOUT),
                 'transmissor_id': self.id, 'header': self.get_header(service, date_now),
                 'request': self.get_request(service, date_now),
                 'response': self.get_response(service, date_now), 'service': service,
                 'url': URLS_ESOCIAL[config.ESOCIAL_TP_AMB][service]['url'],
                 'action': URLS_ESOCIAL[config.ESOCIAL_TP_AMB][service]['action'],
                 'cert': self.transmissor.certificado.cert_pem_file(),
                 'key': self.transmissor.certificado.key_pem_file(), 'capath': self.transmissor.certificado.capath(),
                 'timeout': int(config.ESOCIAL_TIMEOUT)}

        if self.transmissor.certificado and self.protocolo:

            save_file(dados['request'], self.make_retrieve())
            save_file(self.get_command(service, date_now), COMMAND_CURL % dados)
            os.system(COMMAND_CURL % dados)

            if not os.path.isfile(dados['response']):

                self.status = STATUS_TRANSMISSOR_ERRO_CONSULTA
                self.save()

                return {
                    'status': 'error',
                    'mensagem': '''Não foi recebida nenhuma resposta do servidor. 
                        Verifique se a pasta /arquivos/ está com permissão de escrita ou 
                        pode ter ocorrido erro de timeout.
                        Timeout atual %(timeout)s''' % dados}

            elif 'HTTP/1.1 200 OK' not in read_file(dados['header']):

                self.status = STATUS_TRANSMISSOR_ERRO_CONSULTA
                self.save()

                return {
                    'status': 'warning',
                    'mensagem': 'Retorno do servidor: ' + read_file(dados['header'])}

            else:

                TransmissorEventosArquivos(
                    transmissor_evento=self,
                    arquivo=dados['header'],
                    servico=SERVICO_CONSULTAR,
                    tipo=ARQUIVO_TIPO_HEADER,
                    conteudo=read_file(dados['header'])).save()

                TransmissorEventosArquivos(
                    transmissor_evento=self,
                    arquivo=dados['request'],
                    servico=SERVICO_CONSULTAR,
                    tipo=ARQUIVO_TIPO_REQUEST,
                    conteudo=read_file(dados['request'])).save()

                TransmissorEventosArquivos(
                    transmissor_evento=self,
                    arquivo=dados['response'],
                    servico=SERVICO_CONSULTAR,
                    tipo=ARQUIVO_TIPO_RESPONSE,
                    conteudo=read_file(dados['response'])).save()

                soup = BeautifulSoup(read_file(dados['response']), 'xml')
                text = soup.find('retornoProcessamentoLoteEventos').prettify()
                response_dict = xmltodict.parse(text)
                response_json = json.dumps(response_dict)

                self.status = STATUS_TRANSMISSOR_CONSULTADO
                self.retorno_consulta_json = response_json
                self.resposta_codigo = soup.find('cdResposta').text
                self.resposta_descricao = soup.find('descResposta').text
                self.data_hora_consulta = datetime.now()
                self.processamento_versao_aplicativo = soup.find('versaoAplicativoProcessamentoLote').text
                self.arquivo_header = dados['header']
                self.arquivo_request = dados['request']
                self.arquivo_response = dados['response']
                self.save()
                self.transmissor_esocial.update(status=STATUS_EVENTO_PROCESSADO)

                for evt in soup.find_all('evento'):
                    import xml.etree.ElementTree as ET
                    identidade = evt["Id"]
                    retorno_consulta_dict = xmltodict.parse(evt.retornoEvento.prettify())
                    retorno_consulta_json = json.dumps(retorno_consulta_dict)
                    ocorrencias = evt.retornoEvento.eSocial.retornoEvento.processamento.ocorrencias
                    oco_json = None
                    if ocorrencias:
                        oco_dict = xmltodict.parse(ocorrencias.prettify())
                        oco_json = json.dumps(oco_dict)
                    evento = Eventos.objects.get(identidade=identidade)
                    evento.retorno_consulta_json = retorno_consulta_json
                    evento.ocorrencias_json = oco_json
                    if oco_json and oco_json != '{}':
                        evento.status = STATUS_EVENTO_ENVIADO_ERRO
                    evento.save()

                return {
                    'status': 'success',
                    'mensagem': 'Lote consultado com sucesso!'}

        elif not self.protocolo:
            return {
                'status': 'error',
                'mensagem': '''O transmissor ainda não possui um número de protocolo!'''}

        else:
            return {
                'status': 'error',
                'mensagem': '''O certificado não está configurado ou não
                                   possuem eventos validados para envio neste lote!'''}

    def __str__(self):
        return '{} - {}'.format(
            self.id,
            self.transmissor.nome_empresa, )

    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'


class TransmissorEventosSerializer(BaseModelSerializer):
    class Meta:
        model = TransmissorEventos


class TransmissorEventosArquivos(BaseModelEsocial):
    cols = {
        'transmissor_evento': 12,
        'arquivo': 12,
        'servico': 6,
        'tipo': 6,
        'conteudo': 12,
        'created_at': 3,
        'created_by': 3,
        'updated_at': 3,
        'updated_by': 3,
    }
    transmissor_evento = models.ForeignKey(
        'TransmissorEventos',
        on_delete=models.CASCADE,
        related_name='%(class)s_transmissor_evento',
        blank=True, null=True, )
    arquivo = models.CharField('Nome do arquivo', max_length=200, )
    servico = models.IntegerField('Serviço', choices=SERVICOS, )
    tipo = models.IntegerField('Tipo', choices=ARQUIVOS_TIPOS, )
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
        'users': 12,
        'created_at': 3,
        'created_by': 3,
        'updated_at': 3,
        'updated_by': 3,
    }
    nome = models.CharField('Nome', max_length=300, )
    fs_certificado = FileSystemStorage(location=os.path.join(settings.BASE_DIR, settings.CERT_PATH))
    certificado = models.FileField('Arquivo', storage=fs_certificado)
    senha = models.CharField('Senha', max_length=300, blank=True, null=True, )
    users = models.ManyToManyField(User, verbose_name='Usuários', related_name='certificado_users', blank=True,
                                   help_text="Informe a lista de usuários que tem acesso a utilizar este certificado.")

    def cert_pem_file(self):
        file = os.path.join(settings.BASE_DIR, settings.CERT_PATH, 'cert_{}.pem'.format(self.id))
        if not file:
            self.create_pem_files()
        return file

    def key_pem_file(self):
        file = os.path.join(settings.BASE_DIR, settings.CERT_PATH, 'key_{}.pem'.format(self.id))
        if not file:
            self.create_pem_files()
        return file

    def cert_host(self):
        return os.path.join(settings.BASE_DIR, settings.CERT_PATH, self.certificado.name)

    def capath(self):
        return os.path.join(settings.BASE_DIR, 'cacerts', 'esocial')

    def create_pem_files(self):
        import os
        from OpenSSL import crypto

        pkcs12 = crypto.load_pkcs12(
            open(self.cert_host(), 'rb').read(),
            self.senha)

        key_str = crypto.dump_privatekey(
            crypto.FILETYPE_PEM, pkcs12.get_privatekey())
        cert_str = crypto.dump_certificate(
            crypto.FILETYPE_PEM, pkcs12.get_certificate())

        if not os.path.isfile(self.cert_pem_file()):
            cert_str = crypto.dump_certificate(
                crypto.FILETYPE_PEM, pkcs12.get_certificate())
            open(self.cert_pem_file(), 'wb').write(cert_str)

        if not os.path.isfile(self.key_pem_file()):
            key_str = crypto.dump_privatekey(
                crypto.FILETYPE_PEM, pkcs12.get_privatekey())
            open(self.key_pem_file(), 'wb').write(key_str)

        return {
            'key_str': key_str,
            'cert_str': cert_str, }

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Certificados'
        verbose_name_plural = 'Certificados'
        ordering = [
            'nome', ]


# @receiver(post_save, sender=Certificados)
# def save_cert(sender, instance, **kwargs):
#     instance.create_pem_files()


class CertificadosSerializer(BaseModelSerializer):
    class Meta:
        model = Certificados


class Eventos(BaseModelEsocial):
    from .choices import ESOCIAL_VERSAO_DEFAULT
    cols = {
        'versao': 2,
        'evento': 4,
        'operacao': 3,
        'identidade': 3,
        'evento_json': 12,
        'certificado': 4,
    }
    identidade = models.CharField('Identidade',
                                  max_length=36,
                                  blank=True,
                                  null=True,
                                  unique=True)
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
        'Número de inscrição',
        max_length=15,
        help_text="O CNPJ completo somente pode ser utilizado por órgãos públicos, " \
                  "os demais empregadores deverão informar somente o CNPJ base (8 primeiros dígitos do CNPJ)" )
    tpamb = models.IntegerField(
        'Identificação do ambiente',
        choices=CHOICES_TPAMB, default=2)
    procemi = models.IntegerField(
        'Processo de emissão do evento',
        choices=CHOICES_PROCEMI, default=1, )
    verproc = models.CharField(
        'Versão do processo',
        max_length=20, null=True, )
    certificado = models.ForeignKey(
        'Certificados',
        on_delete=models.PROTECT,
        verbose_name='Certificado',
        related_name='certificado_esocial',
        blank=True, null=True, )

    #####

    transmissor_evento = models.ForeignKey(
        'TransmissorEventos',
        on_delete=models.PROTECT,
        verbose_name='Lote/Transmissor',
        related_name='transmissor_esocial',
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
        verbose_name='Lote/Transmissor (Erro)',
        related_name='%(class)s_transmissor_eventos_erros',
        blank=True, )

    retorno_envio_json = models.TextField(
        'Retorno do envio',
        "retorno_envio_json", default='{}', blank=True)
    retorno_consulta_json = models.TextField(
        'Retorno da consulta',
        "retorno_consulta_json", default='{}', blank=True)
    evento_json = models.TextField("JSON", null=True, blank=True)
    evento_xml = models.TextField("XML", null=True, blank=True)
    ocorrencias_json = models.TextField("Ocorrências", null=True, blank=True)
    origem = models.IntegerField(
        'Origem do evento',
        choices=EVENTO_ORIGEM, default=0, )
    is_aberto = models.BooleanField(
        'Está aberto para edição', default=True, )

    def retorno_envio(self):
        return json.loads(self.retorno_envio_json or '{}')

    def retorno_consulta(self):
        return json.loads(self.retorno_consulta_json or '{}')

    def ocorrencias(self):
        return json.loads(self.ocorrencias_json or '{}')

    def __str__(self):
        return self.identidade

    def make_identidade(self, request=None):
        existe = True
        num = 0
        while existe:
            num += 1
            identidade_temp = 'ID{}{:0<14}{}{:0>5}'.format(
                self.tpinsc,
                self.nrinsc,
                self.created_at.strftime('%Y%m%d%H%M%S'),
                num)
            lista_eventos = Eventos.objects.exclude(id=self.id). \
                filter(identidade=identidade_temp).all()
            if not lista_eventos:
                self.identidade = identidade_temp
                self.save()
                existe = False
        return identidade_temp

    def xsd_file(self):
        return os.path.join(
            settings.BASE_DIR,
            'xsd',
            'esocial',
            self.versao,
            '{}.xsd'.format(EVENTO_COD[self.evento]['codigo']))

    def pdf_file(self):
        return os.path.join(settings.BASE_DIR, config.FILES_PATH,
                            'recibos', 'esocial', '{}.pdf'.format(self.identidade))

    def xml_file(self):
        return os.path.join(settings.BASE_DIR, config.FILES_PATH,
                            'eventos', 'esocial', '{}.xml'.format(self.identidade))

    def vincular_transmissor(self, request=None):
        from .models import Eventos, Transmissor, TransmissorEventos
        from .choices import (
            STATUS_EVENTO_AGUARD_ENVIO,
            STATUS_TRANSMISSOR_CADASTRADO,
            EVENTOS_GRUPOS_TABELAS, )

        if not self.transmissor_evento:

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
                self.transmissor_evento = tevt
                self.save()
                return tevt
            else:
                if request:
                    messages.error(
                        request, 'Erro ao vincular evento. Não foi encontrado nenhum transmissor com o número de inscrição: %s!' % self.nrinsc)

    def enviar(self, request=None):
        from .choices import (
            STATUS_TRANSMISSOR_CADASTRADO,
            EVENTOS_GRUPOS_TABELAS, )
        tra = Transmissor.objects. \
            get(nrinsc=self.nrinsc)
        tra_evt_data = {
            'transmissor': tra,
            'empregador_tpinsc': tra.tpinsc,
            'empregador_nrinsc': tra.nrinsc,
            'grupo': EVENTOS_GRUPOS_TABELAS,
            'status': STATUS_TRANSMISSOR_CADASTRADO,
        }
        tra_evt = TransmissorEventos(**tra_evt_data)
        tra_evt.save()
        self.transmissor_evento = tra_evt
        self.save()
        return tra_evt.enviar()

    def assinar(self, request=None):
        import esocial.xml
        import esocial.utils
        from lxml import etree

        if self.certificado:
            certificado = self.certificado
        else:
            if not self.transmissor_evento:
                self.transmissor_evento = self.vincular_transmissor()
            certificado = self.transmissor_evento.certificado
            self.certificado = certificado
            self.save()

        cert_data = esocial.utils.pkcs12_data(
            certificado.certificado.file.name,
            certificado.senha)
        evt = esocial.xml.load_fromfile(self.xml_file())
        evt_signed = esocial.xml.sign(evt, cert_data)
        #xml_header = '<?xml version="1.0" encoding="UTF-8"?>'
        #evt_signed = ''.join([xml_header, etree.tostring(evt_signed).decode("utf-8")])
        evt_signed = etree.tostring(evt_signed).decode("utf-8")
        self.evento_xml = evt_signed
        self.save()
        save_file(self.xml_file(), evt_signed)
        #esocial.xml.dump_tofile(evt_signed, self.xml_file())


        # from signxml import XMLSigner, methods, XMLVerifier
        # if not self.transmissor_evento:
        #     self.vincular_transmissor()
        # cert = self.transmissor_evento.transmissor.certificado.create_pem_files()
        # signed_root = XMLSigner(
        #     method=methods.enveloped,
        #     signature_algorithm='rsa-sha256',
        #     digest_algorithm='sha256',
        #     c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315'). \
        #     sign(xml_obj,
        #          key=cert['key_str'],
        #          cert=cert['cert_str'])
        # #verified_data = XMLVerifier().verify(signed_root).signed_xml
        # return signed_root

    def create_xml(self, request=None):
        from json2xml import json2xml
        from json2xml.utils import readfromstring
        import xml.etree.ElementTree as ET
        from .choices import EVENTO_COD

        data = readfromstring(self.evento_json or '{}')
        wrapper = 'eSocial'
        xml = json2xml.Json2xml(data,
                                wrapper=wrapper, pretty=False,
                                attr_type=False).to_xml().decode()
        evento_codigo = EVENTO_COD[self.evento]['codigo']
        ET.register_namespace("", f"http://www.esocial.gov.br/schema/evt/{evento_codigo}/{self.versao}")
        xml_obj = ET.fromstring(xml)
        xml_obj.set('xmlns', f"http://www.esocial.gov.br/schema/evt/{evento_codigo}/{self.versao}")

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

        xml_obj.find(EVENTO_COD[self.evento]['codigo']).set('Id', self.identidade)
        evento_xml = ET.tostring(xml_obj)
        Eventos.objects.filter(id=self.id).update(evento_xml=evento_xml.decode())
        save_file(self.xml_file(), evento_xml.decode())
        xml_obj = self.assinar()

    def validar(self, request=None):
        from config.functions import validar_schema
        err = validar_schema(self.xsd_file(), self.xml_file())
        err_dict = {}
        err_dict['ocorrencias'] = []
        if err:
            for e in err:
                err_dict['ocorrencias'].append(
                    {"ocorrencia": {'tipo': '1', 'codigo': '-', 'descricao': e.reason, 'localizacao': e.path}})
            self.ocorrencias_json = json.dumps(err_dict)
            self.is_aberto = False
            self.status = STATUS_EVENTO_ENVIADO_ERRO
            self.transmissor_evento = None
            self.save()
            if request:
                messages.error(request, 'Erro na validação do evento!')
        else:
            self.ocorrencias_json = None
            self.is_aberto = False
            self.status = STATUS_EVENTO_AGUARD_ENVIO
            self.save()
            if request:
                messages.success(request, 'Evento validado com sucesso!')

    def duplicar_evento(self, request=None):

        from .choices import STATUS_EVENTO_CADASTRADO
        ev_new = self
        ev_new.status = STATUS_EVENTO_CADASTRADO
        ev_new.identidade = STATUS_EVENTO_CADASTRADO
        ev_new.created_at = datetime.now()
        ev_new.updated_at = None
        ev_new.created_by = None
        ev_new.updated_by = None
        ev_new.id = None
        ev_new.save()
        return ev_new

    def abrir_evento_para_edicao_lista(self):
        return [
            STATUS_EVENTO_CADASTRADO,
            STATUS_EVENTO_VALIDADO_ERRO,
            STATUS_EVENTO_AGUARD_ENVIO,
            STATUS_EVENTO_ENVIADO_ERRO
        ]

    def abrir_evento_para_edicao(self, request=None):
        status_list = self.abrir_evento_para_edicao_lista()
        if self.status in status_list:
            if self.status == STATUS_EVENTO_AGUARD_ENVIO:
                self.status = STATUS_EVENTO_CADASTRADO
            self.is_aberto = True
            self.transmissor_evento = None
            self.save()
            if request:
                messages.success(request, "Evento aberto para edição!")
        else:
            if request:
                messages.error(request, '''
                    Não foi possível abrir o evento para edição! Somente é possível
                    abrir eventos com os seguintes status: "Cadastrado", "Importado", "Validado",
                    "Duplicado", "Erro na validação", "XML Assinado" ou "XML Gerado"
                    ou com o status "Enviado com sucesso" e os seguintes códigos de resposta do servidor:
                    "401 - Lote Incorreto - Erro preenchimento" ou 
                    "402 - Lote Incorreto - schema Inválido"!''')

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        if self.origem == EVENTO_ORIGEM_API and not self.pk:
            self.is_aberto = False
            self.status = STATUS_EVENTO_CADASTRADO
            if self.evento_xml and not self.evento_json:
                import json
                dict = xmltodict.parse(self.evento_xml)
                self.evento_json = json.dumps(dict.get['eSocial'])
            elif self.evento_json and not self.evento_xml:
                from json2xml import json2xml
                from json2xml.utils import readfromstring
                import xml.etree.ElementTree as ET
                from .choices import EVENTO_COD
                data = readfromstring(self.evento_json or '{}')
                wrapper = 'eSocial'
                self.evento_xml = json2xml.Json2xml(data,
                                        wrapper=wrapper, pretty=False,
                                        attr_type=False).to_xml().decode()
        # if self.ocorrencias_json:
        #     self.status = STATUS_EVENTO_ENVIADO_ERRO
        #     if self.transmissor_evento:
        #         self.transmissor_evento_error.add(self.transmissor_evento)
        #     self.transmissor_evento = None
        # elif self.status == STATUS_EVENTO_ENVIADO_ERRO:
        #     self.status = STATUS_EVENTO_CADASTRADO
        super(Eventos, self).save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None)
        if not self.identidade:
            Eventos.objects.filter(id=self.id). \
                update(identidade=self.make_identidade())
        data = Eventos.objects.filter(id=self.id).values().first()
        data['evt'] = self
        data['id'] = None
        EventosHistorico(**data).save()

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


class EventosHistorico(BaseModelEsocial):
    cols = {
        'evento': 8,
        'evento_json': 12,
    }
    evt = models.ForeignKey(
        'Eventos',
        on_delete=models.SET_NULL,
        verbose_name='Evento',
        related_name='evento_esocial',
        blank=True, null=True, )
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
    transmissor_evento = models.ForeignKey(
        'TransmissorEventos',
        on_delete=models.SET_NULL,
        verbose_name='Transmissor',
        related_name='transmissor_esocial_historico',
        blank=True, null=True, )
    certificado = models.ForeignKey(
        'Certificados',
        on_delete=models.SET_NULL,
        verbose_name='Certificado',
        related_name='certificado_esocial_historico',
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
        related_name='%(class)s_arquivo_historico',
        blank=True, )

    transmissor_evento_error = models.ManyToManyField(
        'TransmissorEventos',
        verbose_name='Transmissores (Erro)',
        related_name='%(class)s_transmissor_eventos_erros_historico',
        blank=True, )

    retorno_envio_json = models.TextField(
        'Retorno do envio',
        "retorno_envio_json", default='{}', blank=True)
    retorno_consulta_json = models.TextField(
        'Retorno da consulta',
        "retorno_consulta_json", default='{}', blank=True)
    evento_json = models.TextField("JSON", null=True, blank=True)
    evento_xml = models.TextField("XML", null=True, blank=True)
    ocorrencias_json = models.TextField("Ocorrências", null=True, blank=True)
    origem = models.IntegerField(
        'Origem do evento',
        choices=EVENTO_ORIGEM, default=0, )
    is_aberto = models.BooleanField(
        'Está aberto para edição', default=True, )

    def __str__(self):
        return self.identidade

    class Meta:
        verbose_name = 'Histórico do Evento'
        verbose_name_plural = 'Histórico dos Eventos'
        ordering = [
            'id', ]
