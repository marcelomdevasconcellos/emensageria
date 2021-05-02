from django.contrib import admin
from django.db import models
from django.forms import Select, Textarea
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.contrib import messages
from config.mixins import AuditoriaAdmin, AuditoriaAdminInline, AuditoriaAdminStackedInlineInline

from .models import (
    Certificados,
    Arquivos,
    Relatorios,
    Transmissor,
    TransmissorEventos,
    TransmissorEventosArquivos,
    Eventos,
)
from .forms import (
    EventosForm,
    CertificadosForm,
    ArquivosForm,
)


class CertificadosAdmin(AuditoriaAdmin):
    form = CertificadosForm
    search_fields = (
        'nome',)
    list_display = (
        'nome',)


admin.site.register(Certificados, CertificadosAdmin)


class ArquivosAdmin(AuditoriaAdmin):
    form = ArquivosForm
    search_fields = (
        'arquivo',)
    list_filter = (
        'permite_recuperacao', )
    list_display = (
        'fonte', 
        'arquivo',
        'permite_recuperacao', )
    readonly_fields = (
        'permite_recuperacao',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    )

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Arquivos, ArquivosAdmin)


class RelatoriosAdmin(AuditoriaAdmin):
    search_fields = (
        'titulo', )
    list_filter = ()
    list_display = (
        'titulo', )


admin.site.register(Relatorios, RelatoriosAdmin)


class TransmissorAdmin(AuditoriaAdmin):
    search_fields = (
        'transmissor_tpinsc',
        'transmissor_nrinsc',
        'nome_empresa',
        'nrinsc',
        'tpinsc',)
    list_filter = ()
    list_display = (
        'transmissor_tpinsc',
        'transmissor_nrinsc',
        'nome_empresa',
        'nrinsc',
        'tpinsc',
        'certificado',
    )


admin.site.register(Transmissor, TransmissorAdmin)


class EventosInline(AuditoriaAdminStackedInlineInline):

    classes = ['collapse']
    model = Eventos

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


class TransmissorEventosArquivosInline(AuditoriaAdminStackedInlineInline):

    classes = ['collapse']
    model = TransmissorEventosArquivos

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


class TransmissorEventosAdmin(AuditoriaAdmin):

    def autorizar_envio(modeladmin, request, queryset):
        from .choices import STATUS_TRANSMISSOR_AGUARDANDO
        for obj in queryset:
            obj.status = STATUS_TRANSMISSOR_AGUARDANDO
            obj.save()
    autorizar_envio.short_description = "Autorizar envio de lote"

    def enviar_lote(modeladmin, request, queryset):
        from esocial.transmissor import enviar
        for obj in queryset:
            retorno = enviar(obj)
            retorno['id'] = obj.id
            #self.stdout.write('\n%(id)s %(status)s: %(mensagem)s' % retorno)
            messages.add_message(request, messages.INFO, '%(id)s %(status)s: %(mensagem)s' % retorno)
    enviar_lote.short_description = "Enviar lote"

    def consultar_lote(modeladmin, request, queryset):
        from esocial.transmissor import consultar
        for obj in queryset:
            retorno = consultar(obj)
            retorno['id'] = obj.id
            messages.add_message(request, messages.INFO, '%(id)s %(status)s: %(mensagem)s' % retorno)

    consultar_lote.short_description = "Consultar lote"

    actions = [
        autorizar_envio,
        enviar_lote,
        consultar_lote,
    ]

    inlines = (
        EventosInline,
        TransmissorEventosArquivosInline,
    )

    list_filter = (
        'transmissor',
        'empregador_tpinsc',
        'empregador_nrinsc',
        'grupo',
        'status',)
    list_display = (
        'transmissor',
        'empregador_tpinsc',
        'empregador_nrinsc',
        'grupo',
        'status',
        'resposta_codigo',
        'resposta_descricao',
        'recepcao_data_hora',
        'recepcao_versao_aplicativo',
        'protocolo',
        'processamento_versao_aplicativo',
        'tempo_estimado_conclusao',
        'data_hora_envio',
        'data_hora_consulta',
    )

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(TransmissorEventos, TransmissorEventosAdmin)


class EventosAdmin(AuditoriaAdmin):
    def atualizar_identidade(modeladmin, request, queryset):
        for obj in queryset:
            from .functions import identidade_evento
            Eventos.objects.filter(id=obj.id).\
                update(identidade=identidade_evento(obj))
            messages.add_message(request, messages.INFO, 'Identidade atualizada do evento %s!' % obj.identidade)

    atualizar_identidade.short_description = "Atualizar identidade"

    def autorizar_envio(modeladmin, request, queryset):
        from .functions import autorizar_envio_evento
        for obj in queryset:
            autorizar_envio_evento(obj)
            messages.add_message(request, messages.INFO, 'Autorizado envio do evento %s!' % obj.identidade)

    autorizar_envio.short_description = "Autorizar envio de evento"

    def desvincular_evento_transmissor(modeladmin, request, queryset):
        for obj in queryset:
            Eventos.objects.filter(id=obj.id).\
                update(transmissor_evento=None)
            messages.add_message(request, messages.INFO, '%s desvinculado do transmissor!' % obj.identidade)

    desvincular_evento_transmissor.short_description = "Desvincular evento de transmissor"

    def abrir_evento_edicao(modeladmin, request, queryset):
        from .functions import abrir_evento_para_edicao
        for obj in queryset:
            retorno = abrir_evento_para_edicao(obj)
            if not retorno[0]:
                messages.add_message(request, messages.INFO, retorno[1])
            else:
                messages.add_message(request, messages.ERROR, retorno[1])

    abrir_evento_edicao.short_description = "Abrir evento para edição"

    actions = [
        atualizar_identidade,
        autorizar_envio,
        desvincular_evento_transmissor,
        abrir_evento_edicao,
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
            )
    list_display = (
            'identidade',
            'versao',
            'evento',
            'operacao',
            'status',
    )
    fieldsets = (
        ( None, {
        'fields': (
            'versao', 
            'evento',
            'operacao',
            'identidade', 
            'status',
            'tpinsc',
            'nrinsc',
            'tpamb',
            'procemi',
            'verproc',
            'transmissor_evento',
            'evento_json',
            )
        }),
    )
    readonly_fields = (
        'identidade',
        'transmissor_evento',
        'status',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    )

    def response_change(self, request, obj):
        from django.http import HttpResponseRedirect
        from django.contrib import messages
        from .functions import autorizar_envio_evento
        from .functions import abrir_evento_para_edicao
        from .functions import duplicar_evento
        from .functions import identidade_evento
        
        if "_atualizar_identidade" in request.POST:
            Eventos.objects.filter(id=obj.id).\
                update(identidade=identidade_evento(obj))
            self.message_user(request, "Identidade atualizada com sucesso")
            return HttpResponseRedirect(".")
        
        elif "_duplicar_evento" in request.POST:
            new_obj = duplicar_evento(obj)
            self.message_user(request, "Novo evento criado com sucesso! %s" % new_obj.identidade)
            return HttpResponseRedirect(".")
        
        elif "_abrir_evento_para_edicao" in request.POST:
            retorno = abrir_evento_para_edicao(obj)
            if not retorno[0]:
                self.message_user(request, retorno[1])
            else:
                self.message_user(request, retorno[1], level=messages.ERROR)
            return HttpResponseRedirect(".")
            # Сan also be used (messages.ERROR, messages.WARNING, messages.DEBUG, messages.INFO, messages.SUCCESS)
        
        elif "_autorizar_envio_evento" in request.POST:
            retorno = autorizar_envio_evento(obj)
            if not retorno[0]:
                self.message_user(request, retorno[1])
            else:
                self.message_user(request, retorno[1], level=messages.ERROR)
            return HttpResponseRedirect(".")
        
        return super().response_change(request, obj)
            # incluir redirecionamento para nova url

    # formfield_overrides = {
    #     models.TextField: {
    #         'widget': Textarea(attrs={
    #             'rows': 1,
    #             'cols': 120
    #         })
    #     },
    # }


admin.site.register(Eventos, EventosAdmin)
