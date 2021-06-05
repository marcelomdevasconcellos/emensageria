import json
import os
import re
from datetime import datetime

import xmltodict
from constance import config
from django.apps import apps
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

from config.mixins import BaseModelReinf, BaseModelSerializer, BaseModel
from .choices import *
from config.functions import (create_dir, read_file, save_file)

get_model = apps.get_model


class Arquivos(BaseModelReinf):
    cols = {
        'arquivo': 12,
        'created_at': 3,
        'created_by': 3,
        'updated_at': 3,
        'updated_by': 3,
    }
    fs_arquivo = FileSystemStorage(
        location=os.path.join(settings.BASE_DIR, 'arquivos', 'eventos', 'reinf'))
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


class Relatorios(BaseModelReinf):
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


class Transmissor(BaseModelReinf):
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
        blank=True, null=True)
    endereco_completo = models.TextField(
        'Endereço', null=True, blank=True)
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
        self.transmissor_nrinsc = re.sub('[^0-9]', '', self.transmissor_nrinsc)
        self.nrinsc = re.sub('[^0-9]', '', self.nrinsc)
        super(Transmissor, self).save(**kwargs)

    class Meta:
        verbose_name = 'Transmissor'
        verbose_name_plural = 'Transmissor'


class TransmissorSerializer(BaseModelSerializer):
    class Meta:
        model = Transmissor


class TransmissorEventos(BaseModelReinf):
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
                str(evt.evento_xml))
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

    def enviar(self, service='WsEnviarLoteEventos'):
        from .choices import COMMAND_CURL
        date_now = datetime.now().strftime('%Y%m%d%H%M%S')

        dados = {'quant_eventos': self.quant_eventos(), 'empregador_tpinsc': self.empregador_tpinsc,
                 'empregador_nrinsc': self.empregador_nrinsc, 'transmissor_tpinsc': self.transmissor.transmissor_tpinsc,
                 'transmissor_nrinsc': self.transmissor.transmissor_nrinsc, 'reinf_lote_min': config.REINF_LOTE_MIN,
                 'reinf_lote_max': config.REINF_LOTE_MAX, 'reinf_timeout': int(config.REINF_TIMEOUT),
                 'transmissor_id': self.id, 'header': self.get_header(service, date_now),
                 'request': self.get_request(service, date_now),
                 'response': self.get_response(service, date_now), 'service': service,
                 'url': URLS_REINF[config.REINF_TP_AMB][service]['url'],
                 'action': URLS_REINF[config.REINF_TP_AMB][service]['action'],
                 'cert': self.transmissor.certificado.cert_pem_file(),
                 'key': self.transmissor.certificado.key_pem_file(), 'capath': self.transmissor.certificado.capath(),
                 'timeout': int(config.REINF_TIMEOUT)}

        if self.transmissor.certificado and dados['quant_eventos']:

            if dados['reinf_lote_min'] <= dados['quant_eventos'] <= dados['reinf_lote_max']:

                save_file(dados['request'], self.make_send())
                os.system(COMMAND_CURL % dados)

                if not os.path.isfile(dados['response']):

                    TransmissorEventos.objects.filter(id=self.id). \
                        update(status=STATUS_TRANSMISSOR_ERRO_ENVIO)

                    return {
                        'status': 'error',
                        'mensagem': '''O servidor demorou mais que o esperado
                        para efetuar a conexão! Caso necessário solicite ao
                        administrador do sistema para que aumente o tempo do
                        Timeout. Timeout atual %(timeout)s''' % dados}

                elif 'HTTP/1.1 200 OK' not in read_file(dados['header']):

                    TransmissorEventos.objects.filter(id=self.id). \
                        update(status=STATUS_TRANSMISSOR_ERRO_ENVIO)

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
                resposta_descricao = response_dict.get("status").get("cdResposta")

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
                    return {
                        'status': 'error',
                        'mensagem': '{} {}'.format(
                            resposta_codigo,
                            resposta_descricao)}

                self.status = STATUS_TRANSMISSOR_ENVIADO
                self.save()
                self.transmissor_reinf.update(status=STATUS_EVENTO_ENVIADO)

                return {
                    'status': 'success',
                    'mensagem': '{} {}'.format(
                        resposta_codigo,
                        resposta_descricao)}

            elif dados['quant_eventos'] < dados['reinf_lote_min']:
                return {
                    'status': 'error',
                    'mensagem': 'Lote com quantidade inferior a mínima permitida!'}

            elif dados['quant_eventos'] > dados['reinf_lote_max']:
                return {
                    'status': 'error',
                    'mensagem': 'Lote com quantidade de eventos superior a máxima permitida!'}

            else:
                return {
                    'status': 'error',
                    'mensagem': 'Alguma coisa aconteceu e eu não sei o que foi!'}

        else:
            return {
                'status': 'error',
                'mensagem': '''O certificado não está configurado ou não
                                possuem eventos validados para envio neste lote!'''}

    def consultar(self, service='WsConsultarLoteEventos'):

        from bs4 import BeautifulSoup
        date_now = datetime.now().strftime('%Y%m%d%H%M%S')
        dados = {'quant_eventos': self.quant_eventos(), 'empregador_tpinsc': self.empregador_tpinsc,
                 'empregador_nrinsc': self.empregador_nrinsc, 'transmissor_tpinsc': self.transmissor.transmissor_tpinsc,
                 'transmissor_nrinsc': self.transmissor.transmissor_nrinsc, 'reinf_lote_min': config.REINF_LOTE_MIN,
                 'reinf_lote_max': config.REINF_LOTE_MAX, 'reinf_timeout': int(config.REINF_TIMEOUT),
                 'transmissor_id': self.id, 'header': self.get_header(service, date_now),
                 'request': self.get_request(service, date_now),
                 'response': self.get_response(service, date_now), 'service': service,
                 'url': URLS_REINF[config.REINF_TP_AMB][service]['url'],
                 'action': URLS_REINF[config.REINF_TP_AMB][service]['action'],
                 'cert': self.transmissor.certificado.cert_pem_file(),
                 'key': self.transmissor.certificado.key_pem_file(), 'capath': self.transmissor.certificado.capath(),
                 'timeout': int(config.REINF_TIMEOUT)}

        if self.transmissor.certificado and self.protocolo:

            save_file(dados['request'], self.make_retrieve())
            os.system(COMMAND_CURL % dados)

            if not os.path.isfile(dados['response']):

                self.status = STATUS_TRANSMISSOR_ERRO_CONSULTA
                self.save()

                return {
                    'status': 'error',
                    'mensagem': '''O servidor demorou mais que o esperado
                    para efetuar a conexão! Caso necessário solicite ao
                    administrador do sistema para que aumente o tempo do
                    Timeout. Timeout atual %(timeout)s''' % dados}

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
                self.transmissor_reinf.update(status=STATUS_EVENTO_PROCESSADO)

                for evt in soup.find_all('evento'):
                    identidade = evt["Id"]
                    retorno_consulta_dict = xmltodict.parse(evt.retornoEvento.prettify())
                    retorno_consulta_json = json.dumps(retorno_consulta_dict)
                    print(1)
                    Eventos.objects.filter(identidade=identidade). \
                        update(retorno_consulta_json=retorno_consulta_json)
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
        return '{} {} {}'.format(self.id, self.grupo, self.get_status_display())

    class Meta:
        verbose_name = 'Transmissor do eSocial'
        verbose_name_plural = 'Transmissor do eSocial'


class TransmissorEventosSerializer(BaseModelSerializer):
    class Meta:
        model = TransmissorEventos


class TransmissorEventosArquivos(BaseModelReinf):
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


class Certificados(BaseModelReinf):
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
    fs_certificado = FileSystemStorage(location=os.path.join(settings.BASE_DIR, config.CERT_PATH))
    certificado = models.FileField('Arquivo', storage=fs_certificado)
    senha = models.CharField('Senha', max_length=300, blank=True, null=True, )

    def cert_pem_file(self):
        file = os.path.join(settings.BASE_DIR, config.CERT_PATH, 'cert_{}.pem'.format(self.id))
        if not file:
            self.create_pem_files()
        return file

    def key_pem_file(self):
        file = os.path.join(settings.BASE_DIR, config.CERT_PATH, 'key{}.pem'.format(self.id))
        if not file:
            self.create_pem_files()
        return file

    def cert_host(self):
        return os.path.join(settings.BASE_DIR, config.CERT_PATH, self.certificado.name)

    def capath(self):
        return os.path.join(settings.BASE_DIR, config.CERT_PATH, 'reinf')

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


class CertificadosSerializer(BaseModelSerializer):
    class Meta:
        model = Certificados


class Eventos(BaseModelReinf):
    cols = {
        'evento': 8,
        'evento_json': 12,
    }
    identidade = models.CharField('Identidade',
                                  max_length=36,
                                  blank=True,
                                  null=True,
                                  unique=True)
    versao = models.CharField('Versão',
                              choices=VERSOES,
                              max_length=20,
                              default=REINF_VERSAO_DEFAULT, )
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
        related_name='transmissor_reinf',
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
    evento_json = models.TextField("JSON", null=True, blank=True)
    evento_xml = models.TextField("XML", null=True, blank=True)
    ocorrencias_json = models.TextField("Ocorrências", null=True, blank=True)

    def __str__(self):
        return self.identidade

    def make_identidade(self):
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

    def xml_file(self):
        return os.path.join(settings.BASE_DIR, 'arquivos', 'eventos', 'reinf', '{}.xml'.format(self.identidade))

    def vincular_transmissor(self):
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
                self.status = STATUS_EVENTO_AGUARD_ENVIO
                self.save()
                return (0, 'Evento vinculado com sucesso ao transmissor!')
            else:
                return (1, '''Erro ao vincular evento. Não foi encontrato 
                    nenhum transmissor com o número de inscrição: 
                    %s !''' % self.nrinsc)
        else:
            return (2, '''Evento já vinculado a um tranmissor''')

    def assinar(self, xml_obj):
        from signxml import XMLSigner, methods
        if not self.transmissor_evento:
            self.vincular_transmissor()
        cert = self.transmissor_evento.transmissor.certificado.create_pem_files()
        signed_root = XMLSigner(
            method=methods.enveloped,
            signature_algorithm='rsa-sha256',
            digest_algorithm='sha256',
            c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315'). \
            sign(xml_obj,
                 key=cert['key_str'],
                 cert=cert['cert_str'])
        return signed_root

    def create_xml(self):
        from json2xml import json2xml
        from json2xml.utils import readfromstring
        import xml.etree.ElementTree as ET
        from .choices import EVENTO_COD

        data = readfromstring(self.evento_json)
        wrapper = 'eSocial'
        xml = json2xml.Json2xml(data,
                                wrapper=wrapper, pretty=False,
                                attr_type=False).to_xml().decode()
        # ET.register_namespace("", f"http://www.reinf.gov.br/schema/evt/evtInfoEmpregador/{self.versao}")
        xml_obj = ET.fromstring(xml)
        xml_obj.set('xmlns', f"http://www.reinf.gov.br/schema/evt/evtInfoEmpregador/{self.versao}")
        xml_obj.find(EVENTO_COD[self.evento]['codigo']).set('Id', self.identidade)

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

        # xml_obj.set('Id', self.identidade)
        xml_obj.find(EVENTO_COD[self.evento]['codigo']).set('Id', self.identidade)
        self.assinar(xml_obj)

        evento_xml = ET.tostring(xml_obj)
        save_file(self.xml_file(), evento_xml)
        Eventos.objects.filter(id=self.id).update(evento_xml=evento_xml.decode("utf-8"))

    def validar(self):
        pass

    def duplicar_evento(self):
        from datetime import datetime
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

    def abrir_evento_para_edicao(self):
        status_list = [
            STATUS_EVENTO_CADASTRADO,
            STATUS_EVENTO_VALIDADO_ERRO,
            STATUS_EVENTO_AGUARD_ENVIO,
            STATUS_EVENTO_ENVIADO_ERRO
        ]
        if self.status in status_list:
            self.status = STATUS_EVENTO_CADASTRADO
            self.transmissor_evento = None
            self.save()
            return (0, "Evento aberto para edição!")
        else:
            return (1, '''
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


class EventosHistorico(BaseModelReinf):
    cols = {
        'evento': 8,
        'evento_json': 12,
    }
    evt = models.ForeignKey(
        'Eventos',
        on_delete=models.PROTECT,
        verbose_name='Evento',
        related_name='evento_esocial',
        blank=True, null=True, )
    identidade = models.CharField('Identidade',
                                  max_length=36,
                                  blank=True,
                                  null=True,)
    versao = models.CharField('Versão',
                              choices=VERSOES,
                              max_length=20,
                              default=REINF_VERSAO_DEFAULT, )
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
        on_delete=models.PROTECT,
        verbose_name='Transmissor',
        related_name='transmissor_esocial_historico',
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

    def __str__(self):
        return self.identidade

    class Meta:
        verbose_name = 'Histórico do Evento'
        verbose_name_plural = 'Histórico dos Eventos'
        ordering = [
            'id', ]
