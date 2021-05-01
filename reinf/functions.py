from .models import Eventos



def save_file(filename, content):
    from config.settings import BASE_DIR
    import codecs
    file = codecs.open(BASE_DIR + filename, "w", "utf-8")
    file.write(content)
    file.close()


def read_file(filename):
    from config.settings import BASE_DIR
    import codecs
    file = codecs.open(BASE_DIR + filename, "r", "utf-8")
    content = file.read()
    file.close()
    return content


def create_folders():
    import os
    from config.settings import BASE_DIR
    from constance import config
    services = [
        'RecepcaoLoteReinf',
        'ConsultasReinf',
        'WsEnviarLoteEventos',
        'WsConsultarLoteEventos',
    ]
    for service in services:
        lista_pastas = [
            '%s%sComunicacao/%s/header/' % (BASE_DIR, config.FILES_PATH, service),
            '%s%sComunicacao/%s/request/' % (BASE_DIR, config.FILES_PATH, service),
            '%s%sComunicacao/%s/response/' % (BASE_DIR, config.FILES_PATH, service),
        ]
        for pasta in lista_pastas:
            if not os.path.exists(pasta):
                os.system('mkdir -p %s' % pasta)


def retirar_pontuacao_cpf_cnpj(cpf_cnpj):
    for a in './-_':
        cpf_cnpj = cpf_cnpj.replace(a, '')
    return cpf_cnpj


def identidade_evento(obj):
    from .models import Eventos
    existe = True
    num = 0

    while existe:
        num += 1
        identidade_temp = 'ID{}{:0<14}{}{:0>5}'.format(
            obj.tpinsc,
            obj.nrinsc,
            obj.created_at.strftime('%Y%m%d%H%M%S'),
            num)
        lista_eventos = Eventos.objects.exclude(id=obj.id).\
                filter(identidade=identidade_temp).all()
        if not lista_eventos:
            obj.identidade = identidade_temp
            obj.save()
            existe = False

    return identidade_temp


def duplicar_evento(obj):
    from datetime import datetime
    from .choices import STATUS_EVENTO_CADASTRADO
    ev_new = {
        'versao': obj.versao,
        'evento': obj.evento,
        'operacao': obj.operacao,
        'status': STATUS_EVENTO_CADASTRADO,
        'tpinsc': obj.tpinsc,
        'nrinsc': obj.nrinsc,
        'tpamb': obj.tpamb,
        'procemi': obj.procemi,
        'verproc': obj.verproc,
        'evento_json': obj.evento_json,
        'created_at': datetime.now(),
    }
    new_obj = Eventos(**ev_new)
    new_obj.save()
    return new_obj


def abrir_evento_para_edicao(obj):
    from .models import Eventos
    from .choices import (
        STATUS_EVENTO_CADASTRADO,
        STATUS_EVENTO_IMPORTADO,
        STATUS_EVENTO_DUPLICADO,
        STATUS_EVENTO_GERADO,
        STATUS_EVENTO_GERADO_ERRO,
        STATUS_EVENTO_ASSINADO,
        STATUS_EVENTO_ASSINADO_ERRO,
        STATUS_EVENTO_VALIDADO,
        STATUS_EVENTO_VALIDADO_ERRO,
        STATUS_EVENTO_AGUARD_PRECEDENCIA,
        STATUS_EVENTO_AGUARD_ENVIO,
        STATUS_EVENTO_ENVIADO,
        STATUS_EVENTO_ENVIADO_ERRO,
        STATUS_EVENTO_PROCESSADO,)

    status_list = [
            STATUS_EVENTO_CADASTRADO,
            STATUS_EVENTO_IMPORTADO,
            STATUS_EVENTO_DUPLICADO,
            STATUS_EVENTO_GERADO,
            STATUS_EVENTO_GERADO_ERRO,
            STATUS_EVENTO_ASSINADO,
            STATUS_EVENTO_ASSINADO_ERRO,
            STATUS_EVENTO_VALIDADO,
            STATUS_EVENTO_VALIDADO_ERRO,
            STATUS_EVENTO_AGUARD_PRECEDENCIA,
            STATUS_EVENTO_AGUARD_ENVIO,
            STATUS_EVENTO_ENVIADO_ERRO
        ]
    
    if obj.status in status_list:
        Eventos.objects.filter(id=obj.id).\
            update(status=STATUS_EVENTO_CADASTRADO)
        return (0, "Evento aberto para edição!")
    else:
        return (1, '''
            Não foi possível abrir o evento para edição! Somente é possível
            abrir eventos com os seguintes status: "Cadastrado", "Importado", "Validado",
            "Duplicado", "Erro na validação", "XML Assinado" ou "XML Gerado"
            ou com o status "Enviado com sucesso" e os seguintes códigos de resposta do servidor:
            "401 - Lote Incorreto - Erro preenchimento" ou 
            "402 - Lote Incorreto - schema Inválido"!''')


def enviar_evento(obj):
    from datetime import datetime
    from .models import Eventos, Transmissor, TransmissorEventos
    from .choices import ( 
        STATUS_EVENTO_CADASTRADO, 
        STATUS_EVENTO_AGUARD_ENVIO,
        STATUS_TRANSMISSOR_CADASTRADO, 
        EVENTOS_GRUPOS_TABELAS, )

    transmissor = Transmissor.objects.\
        filter(nrinsc=obj.nrinsc).all()
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
        new_obj = Eventos.objects.filter(
            id=obj.id).update(
            transmissor_evento_id=tevt.id,
            status=STATUS_EVENTO_AGUARD_ENVIO)
        return (0, 'Evento vinculado com sucesso ao transmissor!')
    else:
        return (1, '''Erro ao vincular evento. Não foi encontrato 
            nenhum transmissor com o número de inscrição: 
            %s !''' % obj.nrinsc)


def create_pem_files(certificado):

    from OpenSSL import crypto
    from config.settings import BASE_DIR
    import os

    pkcs12 = crypto.load_pkcs12(
        open(BASE_DIR + certificado.cert_host(), 'rb').read(), 
        certificado.senha)
    key_str = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkcs12.get_privatekey())
    cert_str = crypto.dump_certificate(crypto.FILETYPE_PEM, pkcs12.get_certificate())
    
    if not os.path.isfile(BASE_DIR + certificado.cert_pem_file()):
        cert_str = crypto.dump_certificate(crypto.FILETYPE_PEM, pkcs12.get_certificate())
        open(BASE_DIR + certificado.cert_pem_file(), 'wb').write(cert_str)

    if not os.path.isfile(BASE_DIR + certificado.key_pem_file()):
        key_str = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkcs12.get_privatekey())
        open(BASE_DIR + certificado.key_pem_file(), 'wb').write(key_str)

    return {
        'key_str': key_str,
        'cert_str': cert_str, }


def assinar(obj, xml_obj):

    from lxml import etree
    from signxml import XMLSigner, methods
    from .models import Eventos
    from constance import config

    from config.settings import BASE_DIR

    cert = create_pem_files(
        obj.transmissor_evento.transmissor.certificado )

    signed_root = XMLSigner(
        method=methods.enveloped,
        signature_algorithm='rsa-sha256',
        digest_algorithm='sha256',
        c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315').\
        sign(xml_obj, 
             key=cert['key_str'], 
             cert=cert['cert_str'])

    return signed_root