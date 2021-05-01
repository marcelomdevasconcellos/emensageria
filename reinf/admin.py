from django.contrib import admin
from django.db import models
from django.forms import Select, Textarea
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from config.mixins import AuditoriaAdmin, AuditoriaAdminInline


from .models import (
    Certificados,
    Arquivos,
    ImportacaoArquivos,
    ImportacaoArquivosEventos,
    Relatorios,
    Transmissor,
    TransmissorEventos,
    Eventos,
)
from .forms import (
    EventosForm,
    CertificadosForm,
    )


class CertificadosAdmin(AuditoriaAdmin):
    form = CertificadosForm
    search_fields = (
        'nome',)
    list_display = (
        'nome',)


admin.site.register(Certificados, CertificadosAdmin)


class ArquivosAdmin(AuditoriaAdmin):
    search_fields = ()
    list_filter = ()
    list_display = ('arquivo', 'data_criacao', 'data_criacao', )


admin.site.register(Arquivos, ArquivosAdmin)


class ImportacaoArquivosAdmin(AuditoriaAdmin):
    search_fields = ()
    list_filter = ()
    list_display = (
        'arquivo',
        'status',
        'data_hora',
        'quant_total',
        'quant_aguardando',
        'quant_processado',
        'quant_importado',
        'quant_erros',
    )


admin.site.register(ImportacaoArquivos, ImportacaoArquivosAdmin)


class ImportacaoArquivosEventosAdmin(AuditoriaAdmin):
    search_fields = ()
    list_filter = ()
    list_display = (
        'importacao_arquivos',
        'arquivo',
        'evento',
        'versao',
        'identidade_evento',
        'identidade',
        'status',
        'data_hora',
        'validacoes',
    )


admin.site.register(ImportacaoArquivosEventos, ImportacaoArquivosEventosAdmin)


class RelatoriosAdmin(AuditoriaAdmin):
    search_fields = ()
    list_filter = ()
    list_display = (
        'titulo',
        'campos',
    )


admin.site.register(Relatorios, RelatoriosAdmin)


class TransmissorAdmin(AuditoriaAdmin):
    search_fields = ()
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


class TransmissorEventosAdmin(AuditoriaAdmin):
        
    def enviar_lote(modeladmin, request, queryset):
        from .choices import STATUS_TRANSMISSOR_AGUARDANDO
        for obj in queryset:
            obj.status = STATUS_TRANSMISSOR_AGUARDANDO
            obj.save()

    enviar_lote.short_description = "Enviar lote"

    actions = [
        enviar_lote,
    ]

    search_fields = ()
    list_filter = ()
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

    def has_delete_permission(self, request, obj=None):
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

    atualizar_identidade.short_description = "Atualizar identidade"

    def enviar_evento(modeladmin, request, queryset):
        from .functions import enviar_evento
        for obj in queryset:
            enviar_evento(obj)

    enviar_evento.short_description = "Enviar evento"

    actions = [
        atualizar_identidade,
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
            'evento_json', 
            )
        }),
    )
    readonly_fields = (
        'identidade',
        'status',
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    )
    def response_change(self, request, obj):
        from django.http import HttpResponseRedirect
        from django.contrib import messages
        from .functions import enviar_evento
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
        
        elif "_enviar_evento" in request.POST:
            retorno = enviar_evento(obj)
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
