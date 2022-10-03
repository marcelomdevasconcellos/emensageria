from django.contrib import admin
from django.contrib import messages
from django.utils.safestring import mark_safe

from config.mixins import AuditoriaAdminEventos, AuditoriaAdminStackedInlineInline, AuditoriaAdminInline
from .choices import (STATUS_EVENTO_CADASTRADO,
                      STATUS_EVENTO_ERRO)
from .forms import (
    EventosForm,
    CertificadosForm,
    ArquivosForm,
    TransmissorForm,
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
    fieldsets = ((None, {
        'fields': ('nome', 'certificado', 'senha',)
    }),)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(CertificadosAdmin, self).get_fieldsets(request, obj)
        if request.user.has_perm('auth.view_user'):
            return ((None, {
                        'fields': ('nome', 'certificado', 'senha',)
                    }), ('Usuários', {
                        'fields': ('users', )
                    }))
        return fieldsets

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        try:
            obj.create_pem_files()
        except Exception as e:
            messages.error(request, 'Erro ao tentar criar as chaves do certificado, ' \
                                    'verifique se o mesmo está com a senha correta. {}'.format(e))


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
    }), )
    form = TransmissorForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(TransmissorAdmin, self).get_fieldsets(request, obj)
        if request.user.has_perm('auth.view_user'):
            return (('Transmissor', {
                        'fields': ('transmissor_tpinsc', 'transmissor_nrinsc',)
                    }), ('Empregador', {
                        'fields': ('nome_empresa', 'logotipo', 'endereco_completo',
                                   'tpinsc', 'nrinsc', 'certificado')
                    }), ('Usuários', {
                        'fields': ('users', )
                    }))
        return fieldsets


admin.site.register(Transmissor, TransmissorAdmin)


class EventosInline(AuditoriaAdminInline):
    classes = ['collapse']
    model = Eventos
    fields = (
        'identidade',
        'versao',
        'evento',
        'operacao',
        'status',
    )

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
            messages.add_message(request, messages.INFO, '%(id)s %(retorno)s: %(mensagem)s' % retorno)
    enviar_lote.short_description = "Enviar lote"

    def consultar_lote(modeladmin, request, queryset):
        for obj in queryset:
            retorno = obj.consultar()
            retorno['id'] = obj.id
            messages.add_message(request, messages.INFO, '%(id)s %(retorno)s: %(mensagem)s' % retorno)

    consultar_lote.short_description = "Consultar lote"

    actions = [
        autorizar_envio,
        enviar_lote,
        consultar_lote,
    ]

    inlines = (
        EventosInline,
        #TransmissorEventosArquivosInline,
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
    fieldsets = (
        (None, {
            'fields': (
                'transmissor',
                'grupo',
                'empregador_tpinsc',
                'empregador_nrinsc',
                'status',
                'resposta_codigo',
                'resposta_descricao',
                'data_hora_envio',
                'data_hora_consulta',
                'recepcao_data_hora',
                'recepcao_versao_aplicativo',
                'protocolo',
                'processamento_versao_aplicativo',
                'tempo_estimado_conclusao',
                'created_at',
                'created_by',
                'updated_at',
                'updated_by',),
        }),
        ('Arquivos', {
            'classes': ('collapse',),
            'fields': ('arquivo_header',
                       'arquivo_request',
                       'arquivo_response',),
        }), )

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(TransmissorEventos, TransmissorEventosAdmin)


class EventosAdmin(AuditoriaAdminEventos):

    def acoes(self, obj):
        from django.urls import reverse
        from .choices import (
            STATUS_EVENTO_ERRO,
            STATUS_EVENTO_ENVIADO,
            STATUS_EVENTO_AGUARD_ENVIO,
            STATUS_EVENTO_PROCESSADO,
            STATUS_EVENTO_CADASTRADO, )

        if obj.status == STATUS_EVENTO_CADASTRADO:
            url = reverse('esocial:validar_evento', kwargs={'pk': obj.pk})
            return mark_safe("<a href='{}' class='btn btn-primary form-control'>"
                             "<i class='fa fa-thumbs-o-up'></i>&nbsp;Validar</a>".format(url))

        elif obj.status in (STATUS_EVENTO_ERRO, STATUS_EVENTO_ERRO):
            url = reverse('admin:esocial_eventos_change', kwargs={'object_id': obj.pk})
            url_recibo = reverse('esocial:eventos_recibo', kwargs={'pk': obj.pk})
            return mark_safe("<a href='{}' class='btn btn-danger form-control'>"
                             "<i class='fa fa-minus-square-o'></i>&nbsp;Corrigir</a>"
                             "<a href='{}' class='btn btn-print form-control'>"
                             "<i class='fa fa-thumbs-o-up'></i>&nbsp;Recibo</a>".format(url, url_recibo))

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
        from .choices import (STATUS_EVENTO_CADASTRADO,
                              STATUS_EVENTO_ERRO)
        for obj in queryset:
            if obj.status in (STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_ERRO):
                obj.identidade = obj.make_identidade()
                obj.save()
                messages.add_message(request, messages.INFO, 'Identidade atualizada do evento %s!' % obj.identidade)

    atualizar_identidade.short_description = "Atualizar identidade"

    def delete_model(modeladmin, request, queryset):
        from .choices import (STATUS_EVENTO_CADASTRADO,
                              STATUS_EVENTO_ERRO)
        n = 0
        for obj in queryset:
            if obj.status in (STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_ERRO):
                n += 1
                obj.delete()
            else:
                messages.add_message(request,
                    messages.ERROR,
                    'Não é possível apagar o evento %s, pois o mesmo está com status %s!' % (
                                         obj.identidade, obj.get_status_display()))
        messages.add_message(request, messages.INFO, '%s eventos apagados!' % n)

    delete_model.short_description = "Remover eventos selecionados"

    def validar(modeladmin, request, queryset):
        from .choices import (STATUS_EVENTO_CADASTRADO,
                              STATUS_EVENTO_ERRO)
        n = 0
        for obj in queryset:
            if obj.status in (STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_ERRO):
                n += 1
                if not obj.transmissor_evento:
                    obj.vincular_transmissor()
                obj.create_xml()
                obj.validar()
        messages.add_message(request, messages.INFO, '%s eventos validados!' % n)

    validar.short_description = "Validar evento"

    # def desvincular_evento_transmissor(modeladmin, request, queryset):
    #     for obj in queryset:
    #         Eventos.objects.filter(id=obj.id).\
    #             update(transmissor_evento=None)
    #         messages.add_message(request, messages.INFO, '%s desvinculado do transmissor!' % obj.identidade)
    #
    # desvincular_evento_transmissor.short_description = "Desvincular evento de transmissor"

    def abrir_evento_edicao(modeladmin, request, queryset):
        for obj in queryset:
            retorno = obj.abrir_evento_para_edicao(request=request)

    abrir_evento_edicao.short_description = "Abrir evento para edição"

    actions = [
        atualizar_identidade,
        validar,
        # desvincular_evento_transmissor,
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
            'tpinsc',
            'nrinsc',
            'tpamb',
            'procemi',
            'verproc',
            'status',
            'transmissor_evento',
            'certificado',
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

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
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
                messages.add_message(request,
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
            retorno = obj.transmissor_evento.consultar(request=request)
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
            if not obj.transmissor_evento:
                obj.vincular_transmissor(request=request)
            obj.create_xml(request=request)
            obj.validar(request=request)
            return HttpResponseRedirect(".")
        
        return super().response_change(request, obj)


admin.site.register(Eventos, EventosAdmin)
