import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from reportlab.lib import utils
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from .choices import (
    STATUS_EVENTO_IMPORTADO,
    STATUS_EVENTO_CADASTRADO,
    STATUS_EVENTO_AGUARD_ENVIO,
    STATUS_EVENTO_ENVIADO,
    STATUS_EVENTO_ERRO,
    STATUS_EVENTO_PROCESSADO, )
from .models import (
    Eventos,
    TransmissorEventos,
    Arquivos,
    Relatorios, )


@login_required
def dashboard_json(request):
    import json
    eventos_importados = Eventos.objects.filter(status=STATUS_EVENTO_IMPORTADO)
    eventos_cadastrados = Eventos.objects.filter(status=STATUS_EVENTO_CADASTRADO)
    eventos_erros = Eventos.objects.filter(status=STATUS_EVENTO_ERRO)
    eventos_validados = Eventos.objects.filter(status__in=(STATUS_EVENTO_AGUARD_ENVIO,))
    eventos_enviados = Eventos.objects.filter(status=STATUS_EVENTO_ENVIADO)
    eventos_processados = Eventos.objects.filter(status=STATUS_EVENTO_PROCESSADO)
    dashboars_data = {
        'esocial_quant_cadastrados': eventos_cadastrados.count(),
        'esocial_quant_erros': eventos_erros.count(),
        'esocial_quant_importados': eventos_importados.count(),
        'esocial_quant_validados': eventos_validados.count(),
        'esocial_quant_enviados': eventos_enviados.count(),
        'esocial_quant_processados': eventos_processados.count(),
        'esocial_cadastrados': list(eventos_cadastrados.values('id', 'evento', 'identidade')),
        'esocial_erros': list(eventos_erros.values('id', 'evento', 'identidade')),
        'esocial_validados': list(eventos_validados.values('id', 'evento', 'identidade')),
        'esocial_importados': list(eventos_importados.values('id', 'evento', 'identidade')),
        'esocial_enviados': list(eventos_enviados.values('id', 'evento', 'identidade')),
        'esocial_processados': list(eventos_processados.values('id', 'evento', 'identidade')),
    }
    return HttpResponse(json.dumps(dashboars_data, indent=4))


@login_required
def visualizar_xml(request, pk):
    evt = get_object_or_404(Eventos, id=pk)
    if not evt.transmissor_evento:
        evt.vincular_transmissor()
    evt.create_xml()
    response = HttpResponse(
        evt.evento_xml,
        content_type='text/xml')
    # response['Content-Disposition'] = 'attachment; filename="%s.xml"' % evt.identidade
    return response


@login_required
def enviar_evento(request, pk):
    evt = get_object_or_404(Eventos, id=pk)
    response = evt.enviar()
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
def validar_evento(request, pk):
    evt = get_object_or_404(Eventos, id=pk)
    if evt.evento_json:
        if not evt.transmissor_evento:
            evt = evt.vincular_transmissor()
            evt = Eventos.objects.get(id=pk)
            # print(evt.transmissor_evento)
        evt.create_xml()
        evt.validar()
    else:
        messages.add_message(request, messages.ERROR,
                             'Não é possível validar pois o evento %s não possui dados suficientes!' % evt.identidade)
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse('{}', content_type='application/json')


@login_required
def validar_eventos(request):
    evts = Eventos.objects.filter(status__in=[STATUS_EVENTO_CADASTRADO, STATUS_EVENTO_IMPORTADO])
    for evt in evts:
        if not evt.transmissor_evento:
            evt.vincular_transmissor()
        evt.create_xml()
        evt.validar()
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
    from .choices import STATUS_TRANSMISSOR_AGUARDANDO, STATUS_TRANSMISSOR_CADASTRADO, STATUS_EVENTO_IMPORTADO
    TransmissorEventos.objects.filter(status=STATUS_TRANSMISSOR_CADASTRADO).update(status=STATUS_TRANSMISSOR_AGUARDANDO)
    evt = Eventos.objects.filter(status__in=[STATUS_EVENTO_AGUARD_ENVIO, STATUS_EVENTO_IMPORTADO])
    for e in evt:
        e.vincular_transmissor()
    tes = TransmissorEventos.objects.filter(status=STATUS_TRANSMISSOR_AGUARDANDO).all()
    for te in tes:
        te.enviar()
    if request.META.get('HTTP_REFERER'):
        messages.success(request, 'Lotes enviados')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse('{"mensagem": "Lotes enviados"}',
                        content_type='application/json')


@login_required
def consultar_transmissores(request):
    from .choices import STATUS_TRANSMISSOR_ENVIADO
    tes = TransmissorEventos.objects.filter(status=STATUS_TRANSMISSOR_ENVIADO).all()
    for te in tes:
        te.consultar()
    if request.META.get('HTTP_REFERER'):
        messages.success(request, 'Lotes consultados')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse('{"mensagem": "Lotes consultados"}',
                        content_type='application/json')


@login_required
def transmissores_recibo(request, pk):
    from datetime import datetime
    transmissor_lote_esocial = get_object_or_404(TransmissorEventos, id=pk)
    context = {
        # 'eventos_lista': eventos_lista,
        # 'retorno_envio_json': json.loads(transmissor_lote_esocial.retorno_envio_json),
        # 'retorno_consulta_json': json.loads(transmissor_lote_esocial.retorno_consulta_json),
        # 'ocorrencias_json': json.loads(transmissor_lote_esocial.ocorrencias_json),
        # 'ocorrencias_lista': ocorrencias_lista,
        'transmissor_lote_esocial': transmissor_lote_esocial,
        'data': datetime.now(),
    }
    return render(request, 'transmissores_recibo.html', context)
    # return PDFTemplateResponse(
    #     request=request,
    #     template='transmissores_recibo.html',
    #     filename="transmissores_recibo.pdf",
    #     context=context,
    #     show_content_in_browser=True,
    #     cmd_options={'margin-top': 10,
    #                  'margin-bottom': 10,
    #                  'margin-right': 10,
    #                  'margin-left': 10,
    #                  'zoom': 1,
    #                  'dpi': 72,
    #                  'orientation': 'Landscape',
    #                  "viewport-size": "1366 x 513",
    #                  'javascript-delay': 1000,
    #                  'footer-center': '[page]/[topage]',
    #                  "no-stop-slow-scripts": True}, )


def get_size_image(path):
    img = utils.ImageReader(path)
    return img.getSize()


def pdf_recibo_evento(evento):
    import os
    import json
    from config import settings
    from config.functions import create_dir

    def generate_text_list(texto, compr):
        lista = []
        palavras = texto.split(' ')
        novo_texto = palavras[0]
        del palavras[0]
        for p in palavras:
            if len(novo_texto) + len(p) + 1 > compr:
                lista.append(novo_texto)
                novo_texto = p
            else:
                novo_texto += ' ' + p
        lista.append(novo_texto)
        return lista

    background = os.path.join(settings.BASE_DIR, 'staticfiles', 'recibo', 'recibo_evento.jpg')
    create_dir(evento.pdf_file())

    my_canvas = canvas.Canvas(
        evento.pdf_file(),
        pagesize=A4)
    my_canvas.drawImage(
        background,
        0 * mm, 0 * mm,
        width=210 * mm,
        height=297 * mm, mask='auto')
    if evento.transmissor_evento and evento.transmissor_evento.transmissor.logotipo:
        logo = os.path.join(
            settings.BASE_DIR,
            settings.MEDIA_ROOT,
            evento.transmissor_evento.transmissor.logotipo.file.name)
        logo_w, logo_h = get_size_image(logo)
        my_canvas.drawImage(
            logo, 159 * mm, 280 * mm,
            width=30 * mm, height=(logo_h / logo_w) * 30 * mm)
    my_canvas.setFont('Helvetica', 12)
    my_canvas.drawString(20 * mm, 280 * mm, evento.get_evento_display())
    my_canvas.setFont('Helvetica', 8)
    if evento.transmissor_evento and evento.transmissor_evento.transmissor.logotipo:
        ends = evento.transmissor_evento.transmissor.endereco_completo.replace('\r', '').split('\n')
        ini = 16
        for end in ends:
            my_canvas.drawString(20 * mm, ini * mm, end)
            ini -= 4

    my_canvas.setFont('Helvetica', 9)
    my_canvas.drawString(22 * mm, 252 * mm, evento.identidade)
    my_canvas.drawString(108 * mm, 252 * mm, evento.versao)
    my_canvas.drawString(150 * mm, 252 * mm, evento.get_tpamb_display())
    my_canvas.drawString(22 * mm, 233 * mm, evento.get_procemi_display())
    my_canvas.drawString(79 * mm, 233 * mm, evento.verproc)
    my_canvas.drawString(108 * mm, 233 * mm, evento.get_tpinsc_display())
    my_canvas.drawString(136 * mm, 233 * mm, evento.nrinsc)
    re = json.loads(evento.retorno_consulta_json)

    # RECEPÇÃO
    re = json.loads(evento.retorno_envio_lote_json)
    co = json.loads(evento.retorno_consulta_json)
    if re.get('dadosRecepcaoLote'):
        rec = re.get('dadosRecepcaoLote')
        resp = re.get('status')
        if rec:
            my_canvas.drawString(22 * mm, 214 * mm, rec.get('tpAmb') or '')
            my_canvas.setFont('Helvetica', 9)
            my_canvas.drawString(50 * mm, 214 * mm, rec.get('dhRecepcao') or '')
            my_canvas.setFont('Helvetica', 9)
            my_canvas.drawString(94 * mm, 214 * mm, rec.get('versaoAplicativoRecepcao') or '')
            my_canvas.drawString(122 * mm, 214 * mm, rec.get('protocoloEnvio') or '')
        if not co:
            my_canvas.drawString(22 * mm, 195 * mm, resp.get('cdResposta'))
            my_canvas.drawString(36 * mm, 195 * mm, resp.get('descResposta'))

    # RECEPÇÃO
    if co.get('retornoEvento'):
        rec = co.get('retornoEvento').get('eSocial').get('retornoEvento').get('recepcao')
        if rec:
            my_canvas.drawString(22 * mm, 214 * mm, rec.get('tpAmb') or '')

    # PROCESSAMENTO
    if co.get('retornoEvento'):
        pro = co.get('retornoEvento').get('eSocial').get('retornoEvento').get('processamento')
        if pro:
            my_canvas.drawString(22 * mm, 195 * mm, pro.get('cdResposta'))
            my_canvas.drawString(36 * mm, 195 * mm, pro.get('descResposta'))
            my_canvas.drawString(122 * mm, 195 * mm, pro.get('versaoAppProcessamento') or '')
            my_canvas.drawString(150 * mm, 195 * mm, pro.get('dhProcessamento'))

        # RECIBO
        reci = co.get('retornoEvento').get('eSocial').get('retornoEvento').get('recibo')
        if reci:
            my_canvas.drawString(22 * mm, 176 * mm, reci.get('nrRecibo') or '')
            my_canvas.drawString(79 * mm, 176 * mm, reci.get('hash') or '')

        # OCORRÊNCIAS
        if pro.get('ocorrencias'):
            ocor = pro.get('ocorrencias').get('ocorrencia')
            if not isinstance(ocor, list):
                ocor = [ocor, ]
            ini = 160
            for oco in ocor:
                my_canvas.drawString(22 * mm, ini * mm, oco.get('tipo') or '')
                my_canvas.drawString(32 * mm, ini * mm, oco.get('codigo') or '')
                desc_txt = oco.get('descricao').replace('\n', ' ')
                desc_list = generate_text_list(desc_txt, 88)
                for des in desc_list:
                    my_canvas.drawString(42 * mm, ini * mm, des)
                    ini -= 5
                if oco.get('localizacao'):
                    my_canvas.drawString(42 * mm, ini * mm, oco.get('localizacao') or '')
                else:
                    ini += 5
                ini -= 7
        else:
            ini = 160
            my_canvas.drawString(22 * mm, ini * mm, 'Não há')

    my_canvas.save()


@login_required
def eventos_recibo(request, pk):
    evento = get_object_or_404(Eventos, id=pk)
    pdf_recibo_evento(evento)
    with open(evento.pdf_file(), 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename=' + evento.identidade + '.pdf'
        return response


# @login_required
# def eventos_recibo(request, pk):
#     from datetime import datetime
#     evento = get_object_or_404(Eventos, id=pk)
#     context = {
#         'pk': pk,
#         'evento': evento,
#         'data': datetime.now(),
#         # 'output': output,
#         'user': request.user,
#     }
#     return render(request, 'eventos_recibo.html', context)
#     # return PDFTemplateResponse(
#     #     request=request,
#     #     template='eventos_recibo.html',
#     #     filename="eventos_recibo.pdf",
#     #     context=context,
#     #     show_content_in_browser=True,
#     #     cmd_options={'margin-top': 10,
#     #                  'margin-bottom': 10,
#     #                  'margin-right': 10,
#     #                  'margin-left': 10,
#     #                  'zoom': 1,
#     #                  'dpi': 72,
#     #                  'orientation': 'Landscape',
#     #                  "viewport-size": "1366 x 513",
#     #                  'javascript-delay': 1000,
#     #                  'footer-center': '[page]/[topage]',
#     #                  "no-stop-slow-scripts": True}, )


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
    from django.conf import settings
    from config.functions import read_file
    arquivos = get_object_or_404(Arquivos, id=pk)
    path = os.path.join(settings.BASE_DIR, arquivos.arquivo.name)
    if not os.path.isfile(path):
        messages.error(request, 'Arquivo não encontrado "%s"!' % arquivos.arquivo)
        return redirect('admin:esocial_arquivos_changelist')

    txt = read_file(arquivos.arquivo)
    if '.xml' in arquivos.arquivo:
        return HttpResponse(txt, content_type='text/xml')
    else:
        return HttpResponse(txt, content_type='text/txt')
