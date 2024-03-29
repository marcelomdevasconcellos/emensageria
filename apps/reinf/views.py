import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from rest_framework import generics
from wkhtmltopdf.views import PDFTemplateResponse

from .choices import (
    STATUS_EVENTO_CADASTRADO,
    STATUS_EVENTO_ERRO,
    STATUS_EVENTO_AGUARD_ENVIO,
    STATUS_EVENTO_ENVIADO,
    STATUS_EVENTO_ERRO,
    STATUS_EVENTO_PROCESSADO, )
from .models import (
    Eventos,
    EventosSerializer,
    Transmissor,
    TransmissorEventos,
    Arquivos,
    Relatorios, )


@login_required
def dashboard_json(request):
    import json
    eventos_cadastrados = Eventos.objects.filter(status=STATUS_EVENTO_CADASTRADO)
    eventos_erros_validacao = Eventos.objects.filter(status=STATUS_EVENTO_ERRO)
    eventos_validados = Eventos.objects.filter(status__in=(STATUS_EVENTO_AGUARD_ENVIO,))
    eventos_erros_envio = Eventos.objects.filter(status=STATUS_EVENTO_ERRO)
    eventos_enviados = Eventos.objects.filter(status=STATUS_EVENTO_ENVIADO)
    eventos_processados = Eventos.objects.filter(status=STATUS_EVENTO_PROCESSADO)
    dashboars_data = {
        'reinf_quant_cadastrados': eventos_cadastrados.count(),
        'reinf_quant_erros_validacao': eventos_erros_validacao.count(),
        'reinf_quant_validados': eventos_validados.count(),
        'reinf_quant_erros_envio': eventos_erros_envio.count(),
        'reinf_quant_enviados': eventos_enviados.count(),
        'reinf_quant_processados': eventos_processados.count(),
        'reinf_cadastrados': list(eventos_cadastrados.values('id', 'evento', 'identidade')),
        'reinf_erros_validacao': list(eventos_erros_validacao.values('id', 'evento', 'identidade')),
        'reinf_validados': list(eventos_validados.values('id', 'evento', 'identidade')),
        'reinf_erros_envio': list(eventos_erros_envio.values('id', 'evento', 'identidade')),
        'reinf_enviados': list(eventos_enviados.values('id', 'evento', 'identidade')),
        'reinf_processados': list(eventos_processados.values('id', 'evento', 'identidade')),
    }
    return HttpResponse(json.dumps(dashboars_data, indent=4))


class eventos_api_list(generics.ListCreateAPIView):
    queryset = Eventos.objects.all()
    serializer_class = EventosSerializer

    def perform_create(self, serializer):
        from config.settings import VERSAO_EMENSAGERIA, VERSAO_LAYOUT_REINF
        from constance import config
        serializer.save(
            criado_por=self.request.user,
            tpamb=config.REINF_TP_AMB,
            verproc=VERSAO_EMENSAGERIA,
            procemi=1,
            versao=VERSAO_LAYOUT_REINF,
            arquivo_original=0,
            status=0)

    def perform_update(self, serializer):
        from config.settings import VERSAO_EMENSAGERIA, VERSAO_LAYOUT_REINF
        from constance import config
        serializer.save(
            modificado_por=self.request.user,
            tpamb=config.REINF_TP_AMB,
            verproc=VERSAO_EMENSAGERIA,
            procemi=1,
            versao=VERSAO_LAYOUT_REINF,
            arquivo_original=0,
            status=0)


class eventos_api_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Eventos.objects.all()
    serializer_class = EventosSerializer

    def perform_create(self, serializer):
        from config.settings import VERSAO_EMENSAGERIA, VERSAO_LAYOUT_REINF
        from constance import config
        serializer.save(
            criado_por=self.request.user,
            tpamb=config.REINF_TP_AMB,
            verproc=VERSAO_EMENSAGERIA,
            procemi=1,
            versao=VERSAO_LAYOUT_REINF,
            arquivo_original=0,
            status=0)

    def perform_update(self, serializer):
        from config.settings import VERSAO_EMENSAGERIA, VERSAO_LAYOUT_REINF
        from constance import config
        serializer.save(
            modificado_por=self.request.user,
            tpamb=config.REINF_TP_AMB,
            verproc=VERSAO_EMENSAGERIA,
            procemi=1,
            versao=VERSAO_LAYOUT_REINF,
            arquivo_original=0,
            status=0)


@login_required
def visualizar_xml(request, pk):
    evt = get_object_or_404(Eventos, id=pk)
    evt.vincular_transmissor()
    evt.create_xml()
    response = HttpResponse(
        evt.evento_xml,
        content_type='text/xml')
    # response['Content-Disposition'] = 'attachment; filename="%s.xml"' % evt.identidade
    return response


@login_required
def enviar_evento(request, pk):
    from .choices import (
        STATUS_TRANSMISSOR_CADASTRADO,
        EVENTOS_GRUPOS_TABELAS, )
    evt = get_object_or_404(Eventos, id=pk)
    tra = Transmissor.objects. \
        get(nrinsc=evt.nrinsc)
    tra_evt_data = {
        'transmissor': tra,
        'empregador_tpinsc': tra.tpinsc,
        'empregador_nrinsc': tra.nrinsc,
        'grupo': EVENTOS_GRUPOS_TABELAS,
        'status': STATUS_TRANSMISSOR_CADASTRADO,
    }
    tra_evt = TransmissorEventos(**tra_evt_data)
    tra_evt.save()
    evt.transmissor_evento = tra_evt
    evt.save()
    response = tra_evt.enviar()
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
def validar_eventos(request):
    evts = Eventos.objects.filter(status=STATUS_EVENTO_CADASTRADO)
    for evt in evts:
        evt.create_xml()
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse(json.dumps({}), content_type='application/json')


@login_required
def consultar_evento(request, pk):
    evt = get_object_or_404(Eventos, id=pk)
    response = evt.transmissor_evento.consultar()
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
def enviar_transmissor(request, pk):
    te = get_object_or_404(TransmissorEventos, id=pk)
    response = te.enviar()
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
def consultar_transmissor(request, pk):
    te = get_object_or_404(TransmissorEventos, id=pk)
    response = te.consultar()
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
def enviar_transmissores(request):
    from .choices import STATUS_TRANSMISSOR_AGUARDANDO
    tes = TransmissorEventos.objects.filter(status=STATUS_TRANSMISSOR_AGUARDANDO)
    for te in tes:
        te.enviar()
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse('{}', content_type='application/json')


@login_required
def consultar_transmissores(request):
    from .choices import STATUS_TRANSMISSOR_ENVIADO
    tes = TransmissorEventos.objects.filter(status=STATUS_TRANSMISSOR_ENVIADO)
    for te in tes:
        te.consultar()
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse('{}', content_type='application/json')


@login_required
def transmissores_recibo(request, pk):
    from datetime import datetime
    transmissor_lote_reinf = get_object_or_404(TransmissorEventos, id=pk)
    context = {
        # 'eventos_lista': eventos_lista,
        # 'retorno_envio_json': json.loads(transmissor_lote_reinf.retorno_envio_json),
        # 'retorno_consulta_json': json.loads(transmissor_lote_reinf.retorno_consulta_json),
        # 'ocorrencias_json': json.loads(transmissor_lote_reinf.ocorrencias_json),
        # 'ocorrencias_lista': ocorrencias_lista,
        'transmissor_lote_reinf': transmissor_lote_reinf,
        'data': datetime.now(),
    }
    return PDFTemplateResponse(
        request=request,
        template='transmissores_recibo.html',
        filename="transmissores_recibo.pdf",
        context=context,
        show_content_in_browser=True,
        cmd_options={'margin-top': 10,
                     'margin-bottom': 10,
                     'margin-right': 10,
                     'margin-left': 10,
                     'zoom': 1,
                     'dpi': 72,
                     'orientation': 'Landscape',
                     "viewport-size": "1366 x 513",
                     'javascript-delay': 1000,
                     'footer-center': '[page]/[topage]',
                     "no-stop-slow-scripts": True}, )
    # return render(request, 'transmissores_recibo.html', context)


@login_required
def eventos_recibo(request, pk):
    from datetime import datetime
    evento = get_object_or_404(Eventos, id=pk)
    context = {
        'pk': pk,
        'evento': evento,
        'data': datetime.now(),
        # 'output': output,
        'user': request.user,
    }
    return PDFTemplateResponse(
        request=request,
        template='eventos_recibo.html',
        filename="eventos_recibo.pdf",
        context=context,
        show_content_in_browser=True,
        cmd_options={'margin-top': 10,
                     'margin-bottom': 10,
                     'margin-right': 10,
                     'margin-left': 10,
                     'zoom': 1,
                     'dpi': 72,
                     'orientation': 'Landscape',
                     "viewport-size": "1366 x 513",
                     'javascript-delay': 1000,
                     'footer-center': '[page]/[topage]',
                     "no-stop-slow-scripts": True}, )
    # return render(request, 'eventos_recibo.html', context)


@login_required
def relatorios_imprimir(request, pk, output='pdf'):
    from django.db import connections
    from datetime import datetime

    relatorio = get_object_or_404(Relatorios, id=pk)
    if 'delete' in relatorio.sql.lower() or \
            'insert' in relatorio.sql.lower() or \
            'update' in relatorio.sql.lower() or \
            'drop' in relatorio.sql.lower():
        messages.error(request, '''
            Não foi possível criar o relatório pois o comando SQL contém  
            algumas das seguintes palavras: "DELETE", "UPDATE", "INSERT", "DROP"''')
        return redirect('relatorios')

    if output == 'csv':
        cabecalho = '"%s"\n' % relatorio.campos
        cabecalho = cabecalho.replace(",", '";"')
        cursor = connections['default'].cursor()
        cursor.execute(relatorio.sql)
        row = cursor.fetchall()
        listagem = ''
        for a in row:
            listagem_temp = '";"'.join(a)
            listagem_temp = '"%s"\n' % listagem_temp
            listagem += listagem_temp

    else:
        cabecalho = '<th>%s</th>' % relatorio.campos
        cabecalho = cabecalho.replace(",", "</th><th>")
        cursor = connections['default'].cursor()
        cursor.execute(relatorio.sql)
        row = cursor.fetchall()
        listagem = ''
        for a in row:
            listagem_temp = '</td><td>'.join(a)
            listagem_temp = '<tr><td>%s</td></tr>' % listagem_temp
            listagem += listagem_temp

    context = {
        'relatorio': relatorio,
        'data': datetime.now(),
        'cabecalho': cabecalho,
        'listagem': listagem,
        'output': output,
        'user': request.user,
    }

    if output == 'pdf':
        from wkhtmltopdf.views import PDFTemplateResponse
        return PDFTemplateResponse(
            request=request,
            template='relatorios_imprimir.html',
            filename="relatorios.pdf",
            context=context,
            show_content_in_browser=True,
            cmd_options={'margin-top': 10,
                         'margin-bottom': 10,
                         'margin-right': 10,
                         'margin-left': 10,
                         'zoom': 1,
                         'dpi': 72,
                         'orientation': 'Landscape',
                         "viewport-size": "1366 x 513",
                         'javascript-delay': 1000,
                         'footer-center': '[page]/[topage]',
                         "no-stop-slow-scripts": True}, )

    elif output == 'xls':
        from django.shortcuts import render_to_response
        response = render_to_response('relatorios_imprimir.html', context)
        filename = "relatorios.xls"
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['Content-Type'] = 'application/vnd.ms-excel; charset=UTF-8'
        return response

    elif output == 'csv':
        from django.shortcuts import render_to_response
        response = render_to_response('csv/relatorios.csv', context)
        filename = "relatorios.csv"
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['Content-Type'] = 'text/csv; charset=UTF-8'
        return response

    else:
        return render(request, 'relatorios_imprimir.html', context)


@login_required
def arquivos_visualizar(request, pk):
    import os
    from config.settings import BASE_DIR
    from .functions import read_file
    arquivos = get_object_or_404(Arquivos, id=pk)

    if not os.path.isfile('{}/{}'.format(BASE_DIR, arquivos.arquivo.name)):
        messages.error(request, 'Arquivo não encontrado "%s"!' % arquivos.arquivo)
        return redirect('admin:reinf_arquivos_changelist')

    txt = read_file(arquivos.arquivo)
    if '.xml' in arquivos.arquivo:
        return HttpResponse(txt, content_type='text/xml')
    else:
        return HttpResponse(txt, content_type='text/txt')

# @login_required
# def arquivos_recuperar(request, pk):
#     import os
#     from datetime import datetime
#     from config.mensageiro.functions.funcoes_importacao import importar_arquivo
#     from config.mensageiro.models import ImportacaoArquivosEventos
#     from config.settings import BASE_DIR
#     arquivos = get_object_or_404(Arquivos, id=pk)
#     if arquivos.permite_recuperacao:
#         arquivo_importacao = ImportacaoArquivosEventos.objects.filter(arquivo=arquivos.arquivo).all()

#         if not arquivo_importacao:
#             a = arquivos.arquivo.split('/')
#             nome_arquivo = a[len(a) - 1]
#             path_arq = '/arquivos/Importacao/aguardando/' + nome_arquivo

#             os.system('cp %s %s' % (BASE_DIR + arquivos.arquivo, BASE_DIR + path_arq))

#             arq_import = ImportacaoArquivos.objects. \
#                 filter(arquivo=arquivos.arquivo).all()

#             if arq_import:
#                 obj = arq_import[0]
#             else:
#                 dados_importacao = {}
#                 dados_importacao['arquivo'] = path_arq
#                 dados_importacao['status'] = 0
#                 dados_importacao['data_hora'] = datetime.now()
#                 dados_importacao['quant_processado'] = 0
#                 dados_importacao['quant_erros'] = 0
#                 dados_importacao['quant_aguardando'] = 0
#                 dados_importacao['importado_por_id'] = request.user.id

#                 obj = ImportacaoArquivos(**dados_importacao)
#                 obj.save()

#             dados_eventos = {}
#             dados_eventos['importacao_arquivos_id'] = obj.id
#             dados_eventos['evento'] = '-'
#             dados_eventos['versao'] = '-'
#             dados_eventos['identidade_evento'] = '-'
#             dados_eventos['identidade'] = 0
#             dados_eventos['arquivo'] = path_arq
#             dados_eventos['status'] = 0
#             dados_eventos['data_hora'] = datetime.now()
#             dados_eventos['validacoes'] = ''

#             obj_ev = ImportacaoArquivosEventos(**dados_eventos)
#             obj_ev.save()

#             arquivo_importacao = ImportacaoArquivosEventos.objects.filter(arquivo=path_arq).all()

#         dados_importacao = importar_arquivo(arquivo_importacao[0], request, 0)
#         dados_importacao['status'] = STATUS_IMPORT_PROCESSADO

#         if dados_importacao:
#             messages.warning(request, '''
#                 Arquivo recuperado com sucesso! 
#                 Por gentileza confira todo o conteúdo 
#                 do mesmo, pois este processo não 
#                 passou por validação''')

#         else:
#             messages.error(request, '''
#                 Arquivo não pode ser recuperado 
#                 pois já existe um arquivo com a 
#                 mesma identidade cadastrado!''')

#     else:
#         messages.error(request, 'Este arquivo não permite ser recuperado!')
#     return redirect('arquivos')


# @login_required
# def arquivos_reprocessar(request, pk):

#     import os
#     from config.settings import BASE_DIR

#     arquivos = get_object_or_404(Arquivos, id=pk)

#     texto = ''

#     if not os.path.isfile(BASE_DIR + '/' + arquivos.arquivo):

#         # texto = ler_arquivo(arquivos.arquivo)
#         return redirect('mapa_importacoes', tab='master')

#     a = arquivos.arquivo.split('/')
#     b = a[len(a)-1].split('.')
#     transmissor_id = int(b[0])

#     if 'eSocial' in texto:

#         if 'WsEnviarLoteEventos' in arquivos.arquivo:

#             from config.mensageiro.functions.funcoes_reinf_comunicacao import read_envioLoteEventos
#             read_envioLoteEventos(arquivos.arquivo, transmissor_id)

#         elif 'WsConsultarLoteEventos' in arquivos.arquivo:

#             from config.mensageiro.functions.funcoes_reinf_comunicacao import read_consultaLoteEventos
#             read_consultaLoteEventos(arquivos.arquivo, transmissor_id)

#         messages.success(request, 'Arquivo processado com sucesso!')

#     elif 'Reinf' in texto:

#         if 'RecepcaoLoteReinf' in arquivos.arquivo:
#             from config.mensageiro.functions.funcoes_efdreinf_comunicacao import read_envioLoteEventos
#             read_envioLoteEventos(arquivos.arquivo, transmissor_id)

#         elif 'ConsultasReinf' in arquivos.arquivo:
#             from config.mensageiro.functions.funcoes_efdreinf_comunicacao import read_consultaLoteEventos
#             read_consultaLoteEventos(arquivos.arquivo, transmissor_id)

#         messages.success(request, 'Arquivo processado com sucesso!')

#     else:

#         messages.error(request,
#                        'Não foi possível reprocessar o arquivo!')

#     return redirect('mapa_importacoes', tab='master')
