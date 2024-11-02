from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib import utils
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from apps.esocial.models import Eventos


def get_size_image(
        path):
    img = utils.ImageReader(path)
    return img.getSize()


def pdf_recibo_evento(
        evento):
    import os
    from config import settings
    from config.functions import create_dir

    def generate_text_list(
            texto,
            compr):
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
    my_canvas.setTitle(f"Recibo do Evento - {evento.identidade}")
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

    # RECEPÇÃO
    re = evento.retorno_envio_lote_json
    co = evento.retorno_consulta_json
    if re.get('dadosRecepcaoLote') or re.get('status'):
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
    if co.get('recepcao'):
        rec = co.get('recepcao')
        if rec:
            my_canvas.drawString(22 * mm, 214 * mm, rec.get('tpAmb') or '')

    # PROCESSAMENTO
    if co.get('processamento'):
        pro = co.get('processamento')
        if pro:
            my_canvas.drawString(22 * mm, 195 * mm, pro.get('cdResposta'))
            my_canvas.drawString(36 * mm, 195 * mm, pro.get('descResposta'))
            my_canvas.drawString(122 * mm, 195 * mm, pro.get('versaoAppProcessamento') or '')
            my_canvas.drawString(150 * mm, 195 * mm, pro.get('dhProcessamento'))

        # RECIBO
        reci = co.get('recibo')
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
def eventos_recibo(
        request,
        pk):
    evento = get_object_or_404(Eventos, id=pk)
    pdf_recibo_evento(evento)
    with open(evento.pdf_file(), 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = f'inline; filename={evento.identidade}.pdf'
        response['Content-Title'] = f'Recibo do Evento - {evento.identidade}'
        return response
