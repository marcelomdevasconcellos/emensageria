import datetime

from constance import config
from django.contrib import messages

from .models import STATUS_EVENTO_AGUARD_ENVIO
import xmltodict
import json
from datetime import datetime
from django.apps import apps
from xml.dom import minidom
from config.settings import BASE_DIR
from .models import TransmissorEventos, TransmissorEventosArquivos

import os
from constance import config
from datetime import datetime
from config.settings import BASE_DIR
from .functions import (
    read_file, create_pem_files, 
    create_folders, retirar_pontuacao_cpf_cnpj, save_file)
from django.contrib import messages
from .models import TransmissorEventos, TransmissorEventosArquivos
from .choices import (
    STATUS_TRANSMISSOR_ERRO_ENVIO, 
    STATUS_TRANSMISSOR_ENVIANDO,
    STATUS_TRANSMISSOR_ENVIADO,
    ARQUIVO_TIPO_HEADER,
    ARQUIVO_TIPO_REQUEST,
    ARQUIVO_TIPO_RESPONSE, 
    SERVICO_CONSULTAR,
    SERVICO_ENVIAR,
    URLS_ESOCIAL,
    STATUS_TRANSMISSOR_CONSULTADO,
    )


def consultar(tle, service='WsConsultarLoteEventos'):

    create_folders()
    
    date_now = datetime.now().strftime('%Y%m%d%H%M%S')

    URL_WS = URLS_ESOCIAL[config.ESOCIAL_TP_AMB][service]['url']
    ACTION = URLS_ESOCIAL[config.ESOCIAL_TP_AMB][service]['action']

    if tle.transmissor:
        if tle.transmissor.certificado:
            create_pem_files(tle.transmissor.certificado)
        else:
            return {
                'status': 'error',
                'mensagem': 'O certificado não está configurado ou não possuem eventos validados para envio neste lote!'}
    else:
        return {
            'status': 'error',
            'mensagem': 'O Transmissor não está configurado!'}

    transmissor_dados = {}
    transmissor_dados['empregador_tpinsc'] = tle.empregador_tpinsc
    transmissor_dados['empregador_nrinsc'] = retirar_pontuacao_cpf_cnpj(tle.empregador_nrinsc)
    transmissor_dados['transmissor_tpinsc'] = tle.transmissor.transmissor_tpinsc
    transmissor_dados['transmissor_nrinsc'] = retirar_pontuacao_cpf_cnpj(tle.transmissor.transmissor_nrinsc)
    transmissor_dados['esocial_timeout'] = int(config.ESOCIAL_TIMEOUT)

    dados = {}
    dados['transmissor_id'] = tle.id

    a = (config.FILES_PATH, service, tle.id, date_now)
    dados['header'] = '%sComunicacao/%s/header/%s_%s.txt' % a
    dados['request'] = '%sComunicacao/%s/request/%s_%s.xml' % a
    dados['response'] = '%sComunicacao/%s/response/%s_%s.xml' % a
    dados['service'] = service
    dados['base_dir'] = BASE_DIR
    dados['url'] = URL_WS
    dados['action'] = ACTION
    dados['cert'] = tle.transmissor.certificado.cert_pem_file()
    dados['key'] = tle.transmissor.certificado.key_pem_file()
    dados['cacert'] = BASE_DIR + config.ESOCIAL_CA_CERT_PEM_FILE
    dados['timeout'] = int(config.ESOCIAL_TIMEOUT)

    quant_eventos = tle.quant_eventos()

    if tle.transmissor.certificado and tle.protocolo:

        save_file(dados['request'], tle.make_retrieve)

        command = '''curl 
            --connect-timeout %(timeout)s 
            --insecure 
            --cert %(cert)s 
            --key %(key)s 
            --cacert %(cacert)s 
            -H "Content-Type: text/xml;charset=UTF-8" 
            -H "SOAPAction:%(action)s" 
            --dump-header %(base_dir)s%(header)s 
            --output %(base_dir)s%(response)s 
            -d@%(base_dir)s%(request)s 
            %(url)s''' % dados

        os.system(command.replace('\n', ''))

        if not os.path.isfile(BASE_DIR + dados['response']):

            TransmissorEventos.objects.filter(id=tle.id).\
                update(status=STATUS_TRANSMISSOR_ERRO_CONSULTA)

            return {
                'status': 'error',
                'mensagem': '''O servidor demorou mais que o esperado 
                para efetuar a conexão! Caso necessário solicite ao 
                administrador do sistema para que aumente o tempo do 
                Timeout. Timeout atual %(timeout)s''' % dados}

        elif 'HTTP/1.1 200 OK' not in ler_arquivo(dados['header']):

            TransmissorEventos.objects.filter(id=tle.id).\
                update(status=STATUS_TRANSMISSOR_ERRO_CONSULTA)

            return {
                'status': 'warning',
                'mensagem': 'Retorno do servidor: ' + ler_arquivo(dados['header'])}
                

        else:

            TransmissorEventosArquivos(
                transmissor_evento=tle.id, 
                arquivo=dados['header'], 
                servico=SERVICO_CONSULTAR, 
                tipo=ARQUIVO_TIPO_HEADER, 
                conteudo=read_file(dados['header'])).save()

            TransmissorEventosArquivos(
                transmissor_evento=tle.id, 
                arquivo=dados['request'], 
                servico=SERVICO_CONSULTAR, 
                tipo=ARQUIVO_TIPO_REQUEST, 
                conteudo=read_file(dados['request'])).save()

            TransmissorEventosArquivos(
                transmissor_evento=tle.id, 
                arquivo=dados['response'], 
                servico=SERVICO_CONSULTAR, 
                tipo=ARQUIVO_TIPO_RESPONSE, 
                conteudo=read_file(dados['response'])).save()

            response = xmltodict.parse(read_file(dados['response']))
            response = json.dumps(response)

            TransmissorEventos.objects.filter(id=tle.id).\
                update(
                    status=STATUS_TRANSMISSOR_CONSULTADO, 
                    retorno_consulta_json=response,
                    data_hora_consulta=datetime.now(),
                    arquivo_header=dados['header'],
                    arquivo_request=dados['request'],
                    arquivo_response=dados['response'],)

            return {
                'status': 'success',
                'mensagem': 'Lote consultado com sucesso!'}

            # elif service == 'WsEnviarLoteEventos':
            #     from emensageriapro.mensageiro.functions.funcoes_esocial_comunicacao import read_envioLoteEventos
            #     retorno = read_envioLoteEventos(dados['response'], transmissor_id)
            #     messages.success(request, 'Lote enviado com sucesso! %(resposta_codigo)s - %(resposta_descricao)s' % retorno)

            # elif service == 'WsConsultarLoteEventos':
            #     from emensageriapro.mensageiro.functions.funcoes_esocial_comunicacao import read_consultaLoteEventos
            #     retorno = read_consultaLoteEventos(dados['response'], transmissor_id)
            #     messages.success(request, 'Lote consultado com sucesso! %(resposta_codigo)s - %(resposta_descricao)s' % retorno)


    elif not tle.protocolo:
        return {
                'status': 'error',
                'mensagem': '''O transmissor ainda não possui um número de protocolo!'''}

    else:
        return {
                'status': 'error',
                'mensagem': '''O certificado não está configurado ou não 
                               possuem eventos validados para envio neste lote!'''}



def enviar(tle, service='WsEnviarLoteEventos'):

    TransmissorEventos.objects.filter(id=tle.id).\
        update(status=STATUS_TRANSMISSOR_ENVIANDO)

    create_folders()
    
    date_now = datetime.now().strftime('%Y%m%d%H%M%S')

    URL_WS = URLS_ESOCIAL[config.ESOCIAL_TP_AMB][service]['url']
    ACTION = URLS_ESOCIAL[config.ESOCIAL_TP_AMB][service]['action']

    if tle.transmissor:
        if tle.transmissor.certificado:
            create_pem_files(tle.transmissor.certificado)
        else:
            return {
                'status': 'error',
                'mensagem': 'O certificado não está configurado ou não possuem eventos validados para envio neste lote!'}
    else:
        return {
            'status': 'error',
            'mensagem': 'O Transmissor não está configurado!'}

    transmissor_dados = {}
    transmissor_dados['empregador_tpinsc'] = tle.empregador_tpinsc
    transmissor_dados['empregador_nrinsc'] = retirar_pontuacao_cpf_cnpj(tle.empregador_nrinsc)
    transmissor_dados['transmissor_tpinsc'] = tle.transmissor.transmissor_tpinsc
    transmissor_dados['transmissor_nrinsc'] = retirar_pontuacao_cpf_cnpj(tle.transmissor.transmissor_nrinsc)
    transmissor_dados['esocial_lote_min'] = config.ESOCIAL_LOTE_MIN
    transmissor_dados['esocial_lote_max'] = config.ESOCIAL_LOTE_MAX
    transmissor_dados['esocial_timeout'] = int(config.ESOCIAL_TIMEOUT)

    dados = {}
    dados['transmissor_id'] = tle.id

    a = (config.FILES_PATH, service, tle.id, date_now)
    dados['header'] = '%sComunicacao/%s/header/%s_%s.txt' % a
    dados['request'] = '%sComunicacao/%s/request/%s_%s.xml' % a
    dados['response'] = '%sComunicacao/%s/response/%s_%s.xml' % a
    dados['service'] = service
    dados['base_dir'] = BASE_DIR
    dados['url'] = URL_WS
    dados['action'] = ACTION
    dados['cert'] = tle.transmissor.certificado.cert_pem_file()
    dados['key'] = tle.transmissor.certificado.key_pem_file()
    dados['cacert'] = BASE_DIR + config.ESOCIAL_CA_CERT_PEM_FILE
    dados['timeout'] = int(config.ESOCIAL_TIMEOUT)

    quant_eventos = tle.quant_eventos()

    if tle.transmissor.certificado and quant_eventos:

        if quant_eventos >= transmissor_dados['esocial_lote_min'] and \
            quant_eventos <= transmissor_dados['esocial_lote_max']:

            save_file(dados['request_completo'], tle.make_send)

            command = '''curl 
                --connect-timeout %(timeout)s 
                --insecure 
                --cert %(cert)s 
                --key %(key)s 
                --cacert %(cacert)s 
                -H "Content-Type: text/xml;charset=UTF-8" 
                -H "SOAPAction:%(action)s" 
                --dump-header %(base_dir)s%(header)s 
                --output %(base_dir)s%(response)s 
                -d@%(base_dir)s%(request)s 
                %(url)s''' % dados

            os.system(command.replace('\n', ''))

            if not os.path.isfile(BASE_DIR + dados['response']):

                TransmissorEventos.objects.filter(id=tle.id).\
                    update(status=STATUS_TRANSMISSOR_ERRO_ENVIO)

                return {
                    'status': 'error',
                    'mensagem': '''O servidor demorou mais que o esperado 
                    para efetuar a conexão! Caso necessário solicite ao 
                    administrador do sistema para que aumente o tempo do 
                    Timeout. Timeout atual %(timeout)s''' % dados}

            elif 'HTTP/1.1 200 OK' not in ler_arquivo(dados['header']):

                TransmissorEventos.objects.filter(id=tle.id).\
                    update(status=STATUS_TRANSMISSOR_ERRO_ENVIO)

                return {
                    'status': 'warning',
                    'mensagem': 'Retorno do servidor: ' + ler_arquivo(dados['header'])}

            else:

                TransmissorEventosArquivos(
                    transmissor_evento=tle.id, 
                    arquivo=dados['header'], 
                    servico=SERVICO_ENVIAR, 
                    tipo=ARQUIVO_TIPO_HEADER, 
                    conteudo=read_file(dados['header'])).save()

                TransmissorEventosArquivos(
                    transmissor_evento=tle.id, 
                    arquivo=dados['request'], 
                    servico=SERVICO_ENVIAR, 
                    tipo=ARQUIVO_TIPO_REQUEST, 
                    conteudo=read_file(dados['request'])).save()

                TransmissorEventosArquivos(
                    transmissor_evento=tle.id, 
                    arquivo=dados['response'], 
                    servico=SERVICO_ENVIAR, 
                    tipo=ARQUIVO_TIPO_RESPONSE, 
                    conteudo=read_file(dados['response'])).save()

                response = xmltodict.parse(read_file(dados['response']))
                response = json.dumps(response)

                TransmissorEventos.objects.filter(id=tle.id).\
                    update(
                        status=STATUS_TRANSMISSOR_ENVIADO, 
                        retorno_envio_json=response,
                        data_hora_envio=datetime.now(),
                        arquivo_header=dados['header'],
                        arquivo_request=dados['request'],
                        arquivo_response=dados['response'],)

                return {
                    'status': 'success',
                    'mensagem': 'Lote enviado com sucesso!'}

                # elif service == 'WsEnviarLoteEventos':
                #     from emensageriapro.mensageiro.functions.funcoes_esocial_comunicacao import read_envioLoteEventos
                #     retorno = read_envioLoteEventos(dados['response'], transmissor_id)
                #     messages.success(request, 'Lote enviado com sucesso! %(resposta_codigo)s - %(resposta_descricao)s' % retorno)

                # elif service == 'WsConsultarLoteEventos':
                #     from emensageriapro.mensageiro.functions.funcoes_esocial_comunicacao import read_consultaLoteEventos
                #     retorno = read_consultaLoteEventos(dados['response'], transmissor_id)
                #     messages.success(request, 'Lote consultado com sucesso! %(resposta_codigo)s - %(resposta_descricao)s' % retorno)

        elif quant_eventos < transmissor_dados['esocial_lote_min']:
            return {
                'status': 'error',
                'mensagem': 'Lote com quantidade inferior a mínima permitida!'}

        elif quant_eventos > transmissor_dados['esocial_lote_max']:
            return {
                'status': 'error',
                'mensagem': 'Lote com quantidade de eventos superior a máxima permitida!'}

    else:
        return {
            'status': 'error',
            'mensagem': '''O certificado não está configurado ou não 
                            possuem eventos validados para envio neste lote!'''}