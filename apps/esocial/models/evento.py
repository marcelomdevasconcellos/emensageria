import json
import os
from datetime import datetime
from typing import Any, Dict

import esocial.utils
from django.conf import settings
from django.contrib import messages
from django.db import models
from django.forms import model_to_dict
from esocial.xml import load_fromfile, sign
from json2xml.utils import readfromstring
from lxml import etree

from apps.esocial.choices import (
    CHOICES_INSCRICOESTIPOS, CHOICES_PROCEMI, CHOICES_TPAMB, EVENTOS,
    EVENTOS_GRUPOS_NAO_PERIODICOS,
    EVENTOS_GRUPOS_PERIODICOS, EVENTOS_GRUPOS_TABELAS, EVENTO_COD, EVENTO_ORIGEM, EVENTO_ORIGEM_API,
    EVENTO_ORIGEM_SISTEMA, EVENTO_STATUS, OPERACOES, SIM_NAO, STATUS_EVENTO_AGUARD_ENVIO,
    STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_ERRO, STATUS_EVENTO_IMPORTADO,
    STATUS_TRANSMISSOR_AGUARDANDO, STATUS_TRANSMISSOR_CADASTRADO, VERSOES)
from config.functions import save_file
from config.mixins import BaseModelEsocial
from config.settings import VERSAO_LAYOUT_ESOCIAL


class Eventos(BaseModelEsocial):
    cols = {
        'versao': 2,
        'evento': 4,
        'operacao': 3,
        'identidade': 3,
        'evento_json': 12,
        'certificado': 4,
        'tpinsc': 4,
        'nrinsc': 8,
    }
    identidade = models.CharField(
        'Identidade',
        max_length=36,
        blank=True,
        null=True,
        unique=True)
    versao = models.CharField(
        'Versão',
        choices=VERSOES,
        max_length=20,
        default=VERSAO_LAYOUT_ESOCIAL, )
    evento = models.CharField(
        'Evento',
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
        help_text="O CNPJ completo somente pode ser utilizado por órgãos públicos, "
                  "os demais empregadores deverão informar somente o CNPJ base"
                  " (8 primeiros dígitos do CNPJ)")
    tpamb = models.IntegerField(
        'Identificação do ambiente',
        choices=CHOICES_TPAMB, default=settings.ESOCIAL_TPAMB)
    procemi = models.IntegerField(
        'Processo de emissão do evento',
        choices=CHOICES_PROCEMI, default=settings.ESOCIAL_PROCEMI, )
    verproc = models.CharField(
        'Versão do processo',
        max_length=20, null=True, default=settings.VERSAO_EMENSAGERIA, )
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

    transmissor_evento_error: models.ManyToManyField = models.ManyToManyField(
        'TransmissorEventos',
        verbose_name='Lote/Transmissor (Erro)',
        related_name='%(class)s_transmissor_eventos_erros',
        blank=True, )

    retorno_envio_json = models.JSONField(
        'Retorno do envio', null=True, default=dict, blank=True)
    retorno_consulta_json = models.JSONField(
        'Retorno da consulta', null=True, default=dict, blank=True)
    retorno_envio_lote_json = models.JSONField(
        'Retorno do lote do envio', null=True, default=dict, blank=True)
    retorno_consulta_lote_json = models.JSONField(
        'Retorno do lote da consulta', null=True, default=dict, blank=True)
    evento_json = models.JSONField("JSON", null=True, default=dict, blank=True)
    evento_xml = models.TextField("XML", null=True, blank=True)
    ocorrencias_json = models.JSONField("Ocorrências", default=dict, null=True, blank=True)
    origem = models.IntegerField(
        'Origem do evento',
        choices=EVENTO_ORIGEM, default=EVENTO_ORIGEM_SISTEMA, )
    is_aberto = models.BooleanField(
        'Está aberto para edição', default=True, )

    def get_grupo_esocial(
            self):
        if self.evento in ['s1000', 's1005', 's1010', 's1020', 's1070']:
            return EVENTOS_GRUPOS_TABELAS
        elif self.evento in ['s1200', 's1202', 's1207', 's1210', 's1260', 's1270', 's1280', 's1298',
                             's1299']:
            return EVENTOS_GRUPOS_PERIODICOS
        else:
            return EVENTOS_GRUPOS_NAO_PERIODICOS

    def retorno_envio(
            self):
        return self.retorno_envio_json or {}

    def retorno_consulta(
            self):
        return self.retorno_consulta_json or {}

    def retorno_envio_lote(
            self):
        return self.retorno_envio_lote_json or {}

    def retorno_consulta_lote(
            self):
        return self.retorno_consulta_lote_json or {}

    def ocorrencias(
            self):
        return self.ocorrencias_json or {}

    def __str__(
            self):
        return self.identidade

    def make_identidade(
            self,
            request=None):
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

    def xsd_file(
            self):
        return os.path.join(
            settings.BASE_DIR,
            'xsd',
            'esocial',
            self.versao,
            '{}.xsd'.format(EVENTO_COD[self.evento]['codigo']))

    def pdf_file(
            self):
        return os.path.join(
            settings.MEDIA_ROOT,
            'recibos', 'esocial', '{}.pdf'.format(self.identidade))

    def xml_file(
            self, timestamp=None):
        if timestamp:
            return os.path.join(
                settings.MEDIA_ROOT,
                'eventos', 'esocial', '{}_{}.xml'.format(self.identidade, timestamp))
        return os.path.join(
            settings.MEDIA_ROOT,
            'eventos', 'esocial', '{}.xml'.format(self.identidade))

    def vincular_transmissor(
            self,
            request=None):
        from apps.esocial.models import Transmissor, TransmissorEventos

        if not self.transmissor_evento:

            transmissores = Transmissor.objects. \
                filter(nrinsc=self.nrinsc).all()

            if transmissores:
                transmissor = transmissores[0]
                tevt = TransmissorEventos.objects.filter(
                    empregador_tpinsc=transmissor.tpinsc,
                    empregador_nrinsc=transmissor.nrinsc,
                    grupo=self.get_grupo_esocial(),
                    status=STATUS_TRANSMISSOR_AGUARDANDO).all()
                tra = None
                for t in tevt:
                    evts = Eventos.objects.filter(transmissor_evento=t).all()
                    if len(evts) < settings.ESOCIAL_LOTE_MAX:
                        tra = t
                if not tra:
                    tevt_data = {
                        'transmissor': transmissor,
                        'empregador_tpinsc': transmissor.tpinsc,
                        'empregador_nrinsc': transmissor.nrinsc,
                        'grupo': self.get_grupo_esocial(),
                        'status': STATUS_TRANSMISSOR_CADASTRADO,
                    }
                    tra = TransmissorEventos(**tevt_data)
                    tra.save()
                self.transmissor_evento = tra
                self.save()
                return tra
            else:
                if request:
                    messages.error(
                        request,
                        'Erro ao vincular evento. Não foi encontrado nenhum transmissor'
                        ' com o número de inscrição: %s!' % self.nrinsc)

    def enviar(
            self,
            request=None):
        from apps.esocial.models import Transmissor, TransmissorEventos
        tra = Transmissor.objects. \
            get(nrinsc=self.nrinsc)
        if self.transmissor_evento and self.transmissor_evento.transmissor == tra:
            return self.transmissor_evento.enviar()
        tra_evt_data = {
            'transmissor': tra,
            'empregador_tpinsc': tra.tpinsc,
            'empregador_nrinsc': tra.nrinsc,
            'grupo': self.get_grupo_esocial(),
            'status': STATUS_TRANSMISSOR_CADASTRADO,
        }
        tra_evt = TransmissorEventos(**tra_evt_data)
        tra_evt.save()
        self.transmissor_evento = tra_evt
        self.save()
        return tra_evt.enviar()

    def consultar(
            self,
            request=None):
        if self.transmissor_evento:
            return self.transmissor_evento.consultar()
        else:
            return {}

    def salvar_certificado_transmissor(self):
        if self.transmissor_evento and self.transmissor_evento.transmissor:
            self.certificado = self.transmissor_evento.transmissor.certificado
            self.save()

    def assinar(
            self,
            request=None):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        if not self.transmissor_evento:
            self.vincular_transmissor()
        if self.transmissor_evento and not self.certificado:
            self.salvar_certificado_transmissor()
        if self.transmissor_evento and self.certificado:
            cert_data = esocial.utils.pkcs12_data(
                self.certificado.certificado.file.name,
                self.certificado.get_senha())
            evt = load_fromfile(self.xml_file())
            evt_signed = sign(evt, cert_data)
            evt_signed = etree.tostring(evt_signed).decode("utf-8")
            self.evento_xml = evt_signed
            self.save()
            save_file(self.xml_file(), evt_signed)
            save_file(self.xml_file(timestamp), evt_signed)
        else:
            if request:
                messages.error(
                    request,
                    'Erro ao vincular evento. Não foi encontrado nenhum'
                    ' transmissor com o número de inscrição: %s!' % self.nrinsc)
            return

    def create_xml(
            self,
            request=None):
        import xml.etree.ElementTree as ET
        import dicttoxml
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        wrapper = 'eSocial'
        evento_codigo = EVENTO_COD[self.evento]['codigo']

        if (self.evento_xml and self.origem == EVENTO_ORIGEM_API
                and self.status == STATUS_EVENTO_IMPORTADO):

            xml = self.evento_xml
            if '<eSocial' not in self.evento_xml:
                xml = '<eSocial>' + self.evento_xml + '</eSocial>'

            xml_obj = ET.fromstring(xml)
            if 'www.esocial.gov.br/schema/evt' not in xml:
                ET.register_namespace(
                    "", f"http://www.esocial.gov.br/schema/evt/{evento_codigo}/{self.versao}")
                xml_obj.set(
                    'xmlns', f"http://www.esocial.gov.br/schema/evt/{evento_codigo}/{self.versao}")

            if 'Id="ID' not in xml:
                if not self.identidade:
                    self.make_identidade()
                xml_obj.find(  # type: ignore
                    EVENTO_COD[self.evento]['codigo']).set(
                    'Id', self.identidade)  # type: ignore[arg-type]

            evento_xml = ET.tostring(xml_obj)
            Eventos.objects.filter(id=self.id).update(evento_xml=evento_xml.decode())
            save_file(self.xml_file(), evento_xml.decode())
            save_file(self.xml_file(timestamp), evento_xml.decode())

            if 'Signature' not in self.evento_xml:
                self.assinar(request)

        else:
            data = readfromstring(json.dumps(self.evento_json) or '{}')
            xml = dicttoxml.dicttoxml(
                data,
                attr_type=False,
                custom_root=wrapper,
                item_func=lambda x: x).decode()
            xmlTree = ET.fromstring(xml)
            elemList = []
            for elem in xmlTree.iter():
                elemList.append(elem.tag)
            elemList = list(set(elemList))

            for elem in elemList:  # type: ignore
                xml = xml.replace('<%s><%s>' % (elem, elem), '<%s>' % elem)
                xml = xml.replace('</%s></%s>' % (elem, elem), '</%s>' % elem)

            ET.register_namespace(
                "", f"http://www.esocial.gov.br/schema/evt/{evento_codigo}/{self.versao}")
            xml_obj = ET.fromstring(xml)
            xml_obj.set(
                'xmlns', f"http://www.esocial.gov.br/schema/evt/{evento_codigo}/{self.versao}")

            def recursive_update_datefield(
                    elem2):
                from dateutil import parser as dateutil_parser
                for elem in elem2:
                    if elem.text and len(elem.text) == 10 and len(elem.text.split('/')) == 3:
                        data = dateutil_parser.parse(elem.text, dayfirst=True)
                        elem.text = data.strftime('%Y-%m-%d')
                    else:
                        recursive_update_datefield(elem)

            def recursive_remove(
                    elem2):
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
                    recursive_update_datefield(elem)
                    recursive_remove(elem)
            if self.identidade:
                xml_obj.find(  # type: ignore
                    EVENTO_COD[self.evento]['codigo']).set('Id', self.identidade)
            evento_xml = ET.tostring(xml_obj)
            Eventos.objects.filter(id=self.id).update(evento_xml=evento_xml.decode())
            save_file(self.xml_file(), evento_xml.decode())
            save_file(self.xml_file(timestamp), evento_xml.decode())
            xml_obj = self.assinar(request)

    def validar(
            self,
            request=None):
        from config.functions import validar_schema
        err = validar_schema(self.xsd_file(), self.xml_file())
        err_list = []
        if err:
            for e in err:
                err_list.append(
                    {
                        "ocorrencia": {
                            'tipo': '1',
                            'codigo': '-',
                            'descricao': e.reason,
                            'localizacao': e.path
                        }
                    })
            self.ocorrencias_json = json.dumps(err_list)
            self.is_aberto = False
            self.status = STATUS_EVENTO_ERRO
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

    def duplicar_evento(
            self,
            request=None):
        ev_new = self
        ev_new.status = STATUS_EVENTO_CADASTRADO
        ev_new.identidade = STATUS_EVENTO_CADASTRADO
        ev_new.transmissor_evento = None
        ev_new.created_at = datetime.now()
        ev_new.updated_at = None
        ev_new.created_by = None
        ev_new.updated_by = None
        ev_new.id = None
        ev_new.save()
        return ev_new

    def abrir_evento_para_edicao_lista(
            self):
        return [
            STATUS_EVENTO_IMPORTADO,
            STATUS_EVENTO_CADASTRADO,
            STATUS_EVENTO_ERRO,
            STATUS_EVENTO_AGUARD_ENVIO,
            STATUS_EVENTO_ERRO
        ]

    def abrir_evento_para_edicao(
            self,
            request=None):
        status_list = self.abrir_evento_para_edicao_lista()
        if self.status in status_list:
            if self.status == STATUS_EVENTO_AGUARD_ENVIO or self.status == STATUS_EVENTO_IMPORTADO:
                self.status = STATUS_EVENTO_CADASTRADO
            self.is_aberto = True
            self.transmissor_evento = None
            self.save()
            if request:
                messages.success(request, "Evento aberto para edição!")
        else:
            if request:
                messages.error(
                    request, '''
                    Não foi possível abrir o evento para edição! Somente é possível
                    abrir eventos com os seguintes status: "Cadastrado", "Importado", "Validado",
                    "Duplicado", "Erro na validação", "XML Assinado" ou "XML Gerado"
                    ou com o status "Enviado com sucesso" e os seguintes
                    códigos de resposta do servidor:
                    "401 - Lote Incorreto - Erro preenchimento" ou
                    "402 - Lote Incorreto - schema Inválido"!''')

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None):
        super(Eventos, self).save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None)
        from apps.esocial.models import EventosHistorico
        if not self.identidade:
            self.make_identidade()
        evento = Eventos.objects.get(id=self.id)
        data_dict: Dict[str, Any] = model_to_dict(evento)
        data_dict['evt_id'] = self.pk or None
        data_dict.pop('id', None)
        EventosHistorico(**data_dict).save()

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = [
            'versao',
            'evento',
            'operacao',
            'status', ]
