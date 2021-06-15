from django.contrib import admin
from django.contrib import messages
from django.utils.safestring import mark_safe
from constance import config
from django_currentuser.middleware import get_current_user, get_current_authenticated_user
from config.mixins import AuditoriaAdminEventos, AuditoriaAdminStackedInlineInline
from .forms import (
    EventosForm,
    CertificadosForm,
    ArquivosForm,
)
from .models import (
    Certificados,
    Arquivos,
    Relatorios,
    Transmissor,
    TransmissorEventos,
    TransmissorEventosArquivos,
    Eventos,
)


class CertificadosAdmin(AuditoriaAdminEventos):

    form = CertificadosForm
    search_fields = (
        'nome',)
    list_display = (
        'nome',)


admin.site.register(Certificados, CertificadosAdmin)


class ArquivosAdmin(AuditoriaAdminEventos):
    
    def arquivo_visualizar(self, obj):
        from django.urls import reverse
        url = reverse('esocial:arquivos_visualizar', kwargs={'pk': obj.pk})
        return mark_safe("<a href='{}'>{}</a>".format(url, obj.arquivo.name))

    arquivo_visualizar.allow_tags = True
    arquivo_visualizar.short_description = 'Arquivo'
    arquivo_visualizar.admin_order_field = ['arquivo']

    form = ArquivosForm
    search_fields = (
        'arquivo',)
    list_filter = (
        'permite_recuperacao', )
    list_display = (
        'arquivo_visualizar',
        'fonte', 
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


class RelatoriosAdmin(AuditoriaAdminEventos):

    search_fields = (
        'titulo', )
    list_filter = ()
    list_display = (
        'titulo', )


admin.site.register(Relatorios, RelatoriosAdmin)


class TransmissorAdmin(AuditoriaAdminEventos):

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
    fieldsets = (('Transmissor', {
        'fields': ('transmissor_tpinsc', 'transmissor_nrinsc',)
    }), ('Empregador', {
        'fields': ('nome_empresa', 'logotipo', 'endereco_completo',
                   'tpinsc', 'nrinsc', 'certificado')
    }))


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


class TransmissorEventosAdmin(AuditoriaAdminEventos):
    
    def recibo(self, obj):
        from django.urls import reverse
        url = reverse('esocial:transmissores_recibo', kwargs={'pk': obj.pk})
        return mark_safe("<a href='{}'>Recibo</a>".format(url))

    recibo.allow_tags = True
    recibo.short_description = 'Recibo'

    def autorizar_envio(modeladmin, request, queryset):
        from .choices import STATUS_TRANSMISSOR_AGUARDANDO
        for obj in queryset:
            obj.status = STATUS_TRANSMISSOR_AGUARDANDO
            obj.save()
    autorizar_envio.short_description = "Autorizar envio de lote"

    def enviar_lote(modeladmin, request, queryset):
        for obj in queryset:
            retorno = obj.enviar()
            retorno['id'] = obj.id
            #self.stdout.write('\n%(id)s %(status)s: %(mensagem)s' % retorno)
            messages.add_message(request, messages.INFO, '%(id)s %(status)s: %(mensagem)s' % retorno)
    enviar_lote.short_description = "Enviar lote"

    def consultar_lote(modeladmin, request, queryset):
        for obj in queryset:
            retorno = obj.consultar()
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
        'recibo',
    )

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(TransmissorEventos, TransmissorEventosAdmin)


class EventosAdmin(AuditoriaAdminEventos):

    def acoes(self, obj):
        from django.urls import reverse
        from .choices import (
            STATUS_EVENTO_ENVIADO_ERRO,
            STATUS_EVENTO_VALIDADO_ERRO,
            STATUS_EVENTO_ENVIADO,
            STATUS_EVENTO_AGUARD_ENVIO,
            STATUS_EVENTO_PROCESSADO,
            STATUS_EVENTO_CADASTRADO, )

        if obj.status == STATUS_EVENTO_CADASTRADO:
            url = reverse('esocial:validar_evento', kwargs={'pk': obj.pk})
            return mark_safe("<a href='{}' class='btn btn-primary form-control'>"
                             "<i class='fa fa-thumbs-o-up'></i>&nbsp;Validar</a>".format(url))

        elif obj.status in (STATUS_EVENTO_ENVIADO_ERRO, STATUS_EVENTO_VALIDADO_ERRO):
            url = reverse('admin:esocial_eventos_change', kwargs={'object_id': obj.pk})
            return mark_safe("<a href='{}' class='btn btn-danger form-control'>"
                             "<i class='fa fa-minus-square-o'></i>&nbsp;Corrigir</a>".format(url))

        elif obj.status == STATUS_EVENTO_AGUARD_ENVIO:
            url = reverse('esocial:enviar_evento', kwargs={'pk': obj.pk})
            return mark_safe("<a href='{}' class='btn btn-primary form-control'>"
                             "<i class='fa fa-send-o'></i>&nbsp;Enviar</a>".format(url))

        elif obj.status == STATUS_EVENTO_ENVIADO:
            url = reverse('esocial:consultar_evento', kwargs={'pk': obj.pk})
            url_recibo = reverse('esocial:eventos_recibo', kwargs={'pk': obj.pk})
            return mark_safe("<a href='{}' class='btn btn-primary form-control'>"
                             "<i class='fa fa-search'></i>&nbsp;Consultar</a>"
                             "<a href='{}' class='btn btn-print form-control'>"
                             "<i class='fa fa-thumbs-o-up'></i>&nbsp;Recibo</a>".format(url, url_recibo))

        elif obj.status == STATUS_EVENTO_PROCESSADO:
            url = reverse('esocial:consultar_evento', kwargs={'pk': obj.pk})
            url_recibo = reverse('esocial:eventos_recibo', kwargs={'pk': obj.pk})
            return mark_safe("<a href='{}' class='btn btn-primary form-control'>"
                             "<i class='fa fa-search'></i>&nbsp;Consultar</a>"
                             "<a href='{}' class='btn btn-print form-control'>"
                             "<i class='fa fa-thumbs-o-up'></i>&nbsp;Recibo</a>".format(url, url_recibo))
        else:
            return ''

    acoes.allow_tags = True
    acoes.short_description = 'Ações'

    def atualizar_identidade(modeladmin, request, queryset):
        for obj in queryset:
            obj.identidade = obj.make_identidade()
            obj.save()
            messages.add_message(request, messages.INFO, 'Identidade atualizada do evento %s!' % obj.identidade)

    atualizar_identidade.short_description = "Atualizar identidade"

    def validar(modeladmin, request, queryset):
        for obj in queryset:
            obj.vincular_transmissor()
            obj.create_xml()
            obj.validar()
            messages.add_message(request, messages.INFO, 'Autorizado envio do evento %s!' % obj.identidade)

    validar.short_description = "Autorizar envio de evento"

    def desvincular_evento_transmissor(modeladmin, request, queryset):
        for obj in queryset:
            Eventos.objects.filter(id=obj.id).\
                update(transmissor_evento=None)
            messages.add_message(request, messages.INFO, '%s desvinculado do transmissor!' % obj.identidade)

    desvincular_evento_transmissor.short_description = "Desvincular evento de transmissor"

    def abrir_evento_edicao(modeladmin, request, queryset):
        for obj in queryset:
            retorno = obj.abrir_evento_para_edicao()
            if not retorno[0]:
                messages.add_message(request, messages.INFO, retorno[1])
            else:
                messages.add_message(request, messages.ERROR, retorno[1])

    abrir_evento_edicao.short_description = "Abrir evento para edição"

    actions = [
        atualizar_identidade,
        validar,
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
            'acoes',
    )
    fieldsets = (
        (None, {
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
    #
    # def has_change_permission(self, request, obj=None):
    #     from .choices import STATUS_EVENTO_CADASTRADO
    #     if obj and obj.status != STATUS_EVENTO_CADASTRADO:
    #         return False
    #     return super().has_change_permission(request)

    def has_delete_permission(self, request, obj=None):
        from .choices import STATUS_EVENTO_CADASTRADO
        if obj and obj.status != STATUS_EVENTO_CADASTRADO:
            return False
        return super().has_delete_permission(request)

    def response_change(self, request, obj):
        from django.http import HttpResponseRedirect
        from django.contrib import messages
        
        if "_atualizar_identidade" in request.POST:
            obj.identidade = obj.make_identidade()
            obj.save()
            self.message_user(request, "Identidade atualizada com sucesso %s" % obj.identidade)
            return HttpResponseRedirect(".")
        
        elif "_duplicar_evento" in request.POST:
            retorno = obj.duplicar_evento()
            self.message_user(request, "Novo evento criado com sucesso! %s" % retorno.identidade)
            return HttpResponseRedirect(".")

        elif "_enviar" in request.POST:
            retorno = obj.enviar()
            if retorno['status'] == 'error':
                messages.error(request, retorno['mensagem'])
            elif retorno['status'] == 'warning':
                messages.warning(request, retorno['mensagem'])
            else:
                self.message_user(request, retorno['mensagem'])
            return HttpResponseRedirect(".")

        elif "_consultar" in request.POST:
            retorno = obj.transmissor_evento.consultar()
            if retorno['status'] == 'error':
                messages.error(request, retorno['mensagem'])
            elif retorno['status'] == 'warning':
                messages.warning(request, retorno['mensagem'])
            else:
                self.message_user(request, retorno['mensagem'])
            return HttpResponseRedirect(".")
        
        elif "_abrir_evento_para_edicao" in request.POST:
            retorno = obj.abrir_evento_para_edicao()
            if not retorno[0]:
                self.message_user(request, retorno[1])
            else:
                messages.error(request, retorno[1])
            return HttpResponseRedirect(".")
        
        elif "_validar" in request.POST:
            retorno = obj.vincular_transmissor()
            obj.create_xml()
            obj.validar()
            if not retorno[0]:
                self.message_user(request, retorno[1])
            else:
                messages.error(request, retorno[1])
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
