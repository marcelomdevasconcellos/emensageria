from typing import Any, Dict

from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from apps.esocial.choices import STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_ERRO, \
    STATUS_EVENTO_IMPORTADO
from apps.esocial.forms.evento import EventosForm
from apps.esocial.models import Eventos
from apps.users.models import User
from config.mixins import AuditoriaAdminEventos


def set_nested_value(
        d,
        keys,
        value):
    """
    Insere um valor em um dicionário aninhado de acordo com as chaves.
    Se uma chave termina com `[]`, trata como uma lista.
    """
    for key in keys[:-1]:
        if key not in d:
            d[key] = {}  # Cria novo dicionário para os níveis intermediários
        d = d[key]

    # Verifica se a última chave é uma lista (tem '[]' no final)
    if keys[-1].endswith('[]'):
        final_key = keys[-1].replace('[]', '')
        if final_key not in d:
            d[final_key] = []
        d[final_key].append(value)
    else:
        d[keys[-1]] = value


def convert_form_data_to_json(
        form_data):
    """
    Converte os dados do formulário em um dicionário JSON aninhado,
    respeitando as chaves com '[]' como listas.
    """
    result: Dict[str, Any] = {}

    for key, value in form_data.items():
        # Remove os colchetes e divide as chaves
        keys = key.replace(']', '').split('[')

        # Insere o valor no dicionário aninhado
        set_nested_value(result, keys, value[0])  # Usando o primeiro valor da lista

    return result


@admin.register(Eventos)
class EventosAdmin(AuditoriaAdminEventos):

    @admin.display(description='N. Protocolo')
    def get_protocolo(self, obj):
        retorno = obj.retorno_envio_lote()
        if retorno:
            return retorno.get("dadosRecepcaoLote", {}).get("protocoloEnvio", "")
        return ""

    @admin.display(description='N. Recibo')
    def get_nr_recibo(self, obj):
        retorno = obj.retorno_consulta_lote()
        if retorno:
            return retorno.get("retornoEvento", {}).get("eSocial", {}). \
                get("retornoEvento", {}).get("recibo", {}).get("nrRecibo", "")
        return ""

    @admin.display(description='Ações')
    def acoes(
            self,
            obj):
        from django.urls import reverse
        from apps.esocial.choices import (
            STATUS_EVENTO_IMPORTADO,
            STATUS_EVENTO_ERRO,
            STATUS_EVENTO_ENVIADO,
            STATUS_EVENTO_AGUARD_ENVIO,
            STATUS_EVENTO_PROCESSADO,
            STATUS_EVENTO_CADASTRADO,
        )

        if obj.status in (STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_IMPORTADO):
            url = reverse('esocial:validar_evento', kwargs={'pk': obj.pk})
            return mark_safe(
                "<a href='{}' class='btn btn-primary form-control'>"
                "<i class='fa fa-check'></i>&nbsp;Validar</a>".format(url))

        elif obj.status in (STATUS_EVENTO_ERRO, STATUS_EVENTO_ERRO):
            url = reverse('admin:esocial_eventos_change', kwargs={'object_id': obj.pk})
            url_recibo = reverse('esocial:eventos_recibo', kwargs={'pk': obj.pk})
            return mark_safe(
                "<a href='{}' class='btn btn-danger form-control'>"
                "<i class='fa fa-minus-square-o'></i>&nbsp;Corrigir</a>"
                "<a href='{}' class='btn btn-print form-control'>"
                "<i class='fa fa-print'></i>&nbsp;Recibo</a>".format(url, url_recibo))

        elif obj.status == STATUS_EVENTO_AGUARD_ENVIO:
            url = reverse('esocial:enviar_evento', kwargs={'pk': obj.pk})
            return mark_safe(
                "<a href='{}' class='btn btn-primary form-control'>"
                "<i class='fa fa-send-o'></i>&nbsp;Enviar</a>".format(url))

        elif obj.status == STATUS_EVENTO_ENVIADO:
            url = reverse('esocial:consultar_evento', kwargs={'pk': obj.pk})
            url_recibo = reverse('esocial:eventos_recibo', kwargs={'pk': obj.pk})
            return mark_safe(
                "<a href='{}' class='btn btn-primary form-control'>"
                "<i class='fa fa-search'></i>&nbsp;Consultar</a>"
                "<a href='{}' class='btn btn-print form-control'>"
                "<i class='fa fa-print'></i>&nbsp;Recibo</a>".format(url, url_recibo))

        elif obj.status == STATUS_EVENTO_PROCESSADO:
            url = reverse('esocial:consultar_evento', kwargs={'pk': obj.pk})
            url_recibo = reverse('esocial:eventos_recibo', kwargs={'pk': obj.pk})
            return mark_safe(
                "<a href='{}' class='btn btn-primary form-control'>"
                "<i class='fa fa-search'></i>&nbsp;Consultar</a>"
                "<a href='{}' class='btn btn-print form-control'>"
                "<i class='fa fa-print'></i>&nbsp;Recibo</a>".format(url, url_recibo))
        else:
            return ''

    @admin.display(description='Atualizar identidade')
    def atualizar_identidade(
            modeladmin,
            request,
            queryset):
        from apps.esocial.choices import (
            STATUS_EVENTO_CADASTRADO,
            STATUS_EVENTO_ERRO,
        )
        for obj in queryset:
            if obj.status in (STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_ERRO):
                obj.identidade = obj.make_identidade()
                obj.save()
                messages.add_message(
                    request, messages.INFO,
                    'Identidade atualizada do evento %s!' % obj.identidade)

    @admin.display(description='Remover eventos selecionados')
    def delete_model(
            modeladmin,
            request,
            queryset):
        from apps.esocial.choices import (
            STATUS_EVENTO_CADASTRADO,
            STATUS_EVENTO_ERRO,
            STATUS_EVENTO_IMPORTADO,
        )
        n = 0
        for obj in queryset:
            if obj.status in (
                    STATUS_EVENTO_IMPORTADO, STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_ERRO):
                n += 1
                obj.delete()
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Não é possível apagar o evento %s, pois o mesmo está com status %s!' % (
                        obj.identidade, obj.get_status_display()))
        messages.add_message(request, messages.INFO, '%s eventos apagados!' % n)

    @admin.display(description='Validar evento')
    def validar(
            modeladmin,
            request,
            queryset):
        from apps.esocial.choices import (
            STATUS_EVENTO_CADASTRADO,
            STATUS_EVENTO_ERRO,
        )
        n = 0
        for obj in queryset:
            if obj.status in (
                    STATUS_EVENTO_IMPORTADO, STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_ERRO):
                n += 1
                if not obj.lote:
                    obj.vincular_transmissor()
                obj.create_xml()
                obj.validar()
        messages.add_message(request, messages.INFO, '%s eventos validados!' % n)

    @admin.display(description='Abrir evento para edição')
    def abrir_evento_edicao(
            modeladmin,
            request,
            queryset):
        for obj in queryset:
            obj.abrir_evento_para_edicao(request=request)

    actions = [
        atualizar_identidade,
        validar,
        abrir_evento_edicao,
        delete_model,
    ]

    form = EventosForm
    change_form_template = "eventos.html"
    search_fields = (
        'identidade',
        'evento_json',
    )
    list_filter = (
        'versao',
        'evento',
        'operacao',
        'status',
        'nrinsc',
    )
    list_display = (
        'identidade',
        'versao',
        'evento',
        'operacao',
        'status',
        'get_protocolo',
        'get_nr_recibo',
        'acoes',
    )
    fieldsets = (
        (None, {
            'fields': (
                'versao',
                'evento',
                'operacao',
                'identidade',
                'tpinsc',
                'nrinsc',
                'tpamb',
                'procemi',
                'verproc',
                'status',
                'lote',
                'certificado',
                'evento_json',
            )
        }),
    )
    readonly_fields = (
        'identidade',
        'lote',
        'status',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    )

    def has_delete_permission(
            self,
            request,
            obj=None):
        return False

    def response_change(
            self,
            request,
            obj):
        from django.http import HttpResponseRedirect
        from django.contrib import messages

        if "_atualizar_identidade" in request.POST:
            obj.identidade = obj.make_identidade(request=request)
            obj.save()
            self.message_user(request, "Identidade atualizada com sucesso %s" % obj.identidade)
            return HttpResponseRedirect(".")

        elif "_duplicar_evento" in request.POST:
            retorno = obj.duplicar_evento(request=request)
            self.message_user(request, "Novo evento criado com sucesso! %s" % retorno.identidade)
            return HttpResponseRedirect(".")

        elif "_apagar" in request.POST:
            if obj.status in (STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_ERRO):
                obj.delete()
                return HttpResponseRedirect(".")
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Não é possível apagar o evento %s, pois o mesmo está com status %s!' % (
                        obj.identidade, obj.get_status_display()))

        elif "_enviar" in request.POST:
            retorno = obj.enviar(request=request)
            if retorno['retorno'] == 'error':
                messages.error(request, retorno['mensagem'])
            elif retorno['retorno'] == 'warning':
                messages.warning(request, retorno['mensagem'])
            else:
                self.message_user(request, retorno['mensagem'])
            return HttpResponseRedirect(".")

        elif "_consultar" in request.POST:
            retorno = obj.lote.consultar(request=request)
            if retorno['retorno'] == 'error':
                messages.error(request, retorno['mensagem'])
            elif retorno['retorno'] == 'warning':
                messages.warning(request, retorno['mensagem'])
            else:
                self.message_user(request, retorno['mensagem'])
            return HttpResponseRedirect(".")

        elif "_abrir_evento_para_edicao" in request.POST:
            obj.abrir_evento_para_edicao(request=request)
            return HttpResponseRedirect(".")

        elif "_validar" in request.POST:
            if not obj.lote:
                obj.vincular_transmissor(request=request)
            obj.create_xml(request=request)
            obj.validar(request=request)
            return HttpResponseRedirect(".")

        return super().response_change(request, obj)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # Obtém o usuário autenticado e filtra os slugs dos eventos
        user: User = request.user
        if user.is_superuser:
            return queryset  # Retorna todos os eventos para superusuários
        slugs = user.eventos  # Converte a string de eventos em lista
        return queryset.filter(evento__in=slugs)

    def get_form(self, request, obj=None, change=False, **kwargs):
        """
        Sobrescreve o método `get_form` para passar o usuário atual ao formulário.
        """
        form = super().get_form(request, obj=None, change=False, **kwargs)
        form.current_user = request.user  # type: ignore
        return form
