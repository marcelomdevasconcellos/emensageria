from config.settings import CURL_PATH

TPAMB = {
    'Produção': 1,
    'Produção Restrita': 2,
}

URLS_ESOCIAL = {
    'Produção': {
        'WsEnviarLoteEventos': {
            'url': 'https://webservices.envio.esocial.gov.br/servicos/empregador/'
                   'enviarloteeventos/WsEnviarLoteEventos.svc',
            'action': 'http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/v1_1_0/'
                      'ServicoEnviarLoteEventos/EnviarLoteEventos',
        },
        'WsConsultarLoteEventos': {
            'url': 'https://webservices.consulta.esocial.gov.br/servicos/empregador/'
                   'consultarloteeventos/WsConsultarLoteEventos.svc',
            'action': 'http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/'
                      'consulta/retornoProcessamento/v1_1_0/ServicoConsultarLoteEventos'
                      '/ConsultarLoteEventos',
        },
    },
    'Produção Restrita': {
        'WsEnviarLoteEventos': {
            'url': 'https://webservices.producaorestrita.esocial.gov.br/servicos'
                   '/empregador/enviarloteeventos/WsEnviarLoteEventos.svc',
            'action': 'http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/v1_1_0/'
                      'ServicoEnviarLoteEventos/EnviarLoteEventos',
        },
        'WsConsultarLoteEventos': {
            'url': 'https://webservices.producaorestrita.esocial.gov.br/servicos/empregador/'
                   'consultarloteeventos/WsConsultarLoteEventos.svc',
            'action': 'http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/'
                      'consulta/retornoProcessamento/v1_1_0/ServicoConsultarLoteEventos/'
                      'ConsultarLoteEventos',
        },
    },
}

COMMAND_CURL = CURL_PATH + 'curl --insecure --connect-timeout %(timeout)s ' \
                           '--cert %(cert)s --key %(key)s --capath %(capath)s ' \
                           '-H "Content-Type: text/xml;charset=UTF-8" ' \
                           '-H "SOAPAction:%(action)s" ' \
                           '--dump-header %(header)s ' \
                           '--output %(response)s ' \
                           '-d@%(request)s %(url)s'

MAKE_SEND = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:v1="http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/v1_1_0">
    <soapenv:Header/>
    <soapenv:Body>
        <v1:EnviarLoteEventos><!--Optional:-->
            <v1:loteEventos>
                <eSocial xmlns="http://www.esocial.gov.br/schema/lote/eventos/envio/v1_1_1">
                    <envioLoteEventos grupo="{}">
                        <ideEmpregador>
                            <tpInsc>{}</tpInsc>
                            <nrInsc>{}</nrInsc>
                        </ideEmpregador>
                        <ideTransmissor>
                            <tpInsc>{}</tpInsc>
                            <nrInsc>{}</nrInsc>
                        </ideTransmissor>
                        <eventos>{}</eventos>
                    </envioLoteEventos>
                </eSocial>
            </v1:loteEventos>
        </v1:EnviarLoteEventos>
    </soapenv:Body>
</soapenv:Envelope>"""

MAKE_RETRIEVE = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:v1="http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/consulta/retornoProcessamento/v1_1_0">
    <soapenv:Header/>
    <soapenv:Body>
        <v1:ConsultarLoteEventos>
            <v1:consulta>
                <eSocial xmlns="http://www.esocial.gov.br/schema/lote/eventos/envio/consulta/retornoProcessamento/v1_0_0"
                         xmlns:xs="http://www.w3.org/2001/XMLSchema">
                    <consultaLoteEventos>
                        <protocoloEnvio>{}</protocoloEnvio>
                    </consultaLoteEventos>
                </eSocial>
            </v1:consulta>
        </v1:ConsultarLoteEventos>
    </soapenv:Body>
</soapenv:Envelope>"""  # noqa: E501

STATUS_EVENTO_IMPORTADO = -1
STATUS_EVENTO_CADASTRADO = 0
STATUS_EVENTO_ERRO = 1
STATUS_EVENTO_AGUARD_ENVIO = 2
STATUS_EVENTO_ENVIADO = 3
# STATUS_EVENTO_ERRO = 4
STATUS_EVENTO_PROCESSADO = 5
STATUS_EVENTO_ENVIANDO = 6
STATUS_EVENTO_CONSULTANDO = 7

EVENTO_STATUS = [
    (STATUS_EVENTO_IMPORTADO, 'Importado pela API'),
    (STATUS_EVENTO_CADASTRADO, 'Cadastrado (Aguardando validação)'),
    (STATUS_EVENTO_ERRO, 'Erro (Aguardando correção)'),
    # (STATUS_EVENTO_ERRO, 'Erro (Aguardando correção)'),
    (STATUS_EVENTO_AGUARD_ENVIO, 'Validado (Aguardando envio)'),
    (STATUS_EVENTO_ENVIANDO, 'Enviando ...'),
    (STATUS_EVENTO_ENVIADO, 'Enviado (Aguardando consulta)'),
    (STATUS_EVENTO_CONSULTANDO, 'Consultando ...'),
    (STATUS_EVENTO_PROCESSADO, 'Consultado'),
]

STATUS_TRANSMISSOR_CADASTRADO = 0
STATUS_TRANSMISSOR_AGUARDANDO = 1
STATUS_TRANSMISSOR_ENVIANDO = 2
STATUS_TRANSMISSOR_ENVIADO = 3
STATUS_TRANSMISSOR_ERRO_ENVIO = 4
STATUS_TRANSMISSOR_CONSULTANDO = 5
STATUS_TRANSMISSOR_CONSULTADO = 6
STATUS_TRANSMISSOR_ERRO_CONSULTA = 7

TRANSMISSOR_STATUS = [
    (STATUS_TRANSMISSOR_CADASTRADO, 'Cadastrado'),
    (STATUS_TRANSMISSOR_AGUARDANDO, 'Aguardando envio'),
    (STATUS_TRANSMISSOR_ENVIANDO, 'Enviando ...'),
    (STATUS_TRANSMISSOR_ENVIADO, 'Enviado'),
    (STATUS_TRANSMISSOR_ERRO_ENVIO, 'Erro no envio'),
    (STATUS_TRANSMISSOR_CONSULTANDO, 'Consultando ...'),
    (STATUS_TRANSMISSOR_CONSULTADO, 'Consultado'),
    (STATUS_TRANSMISSOR_ERRO_CONSULTA, 'Erro na consulta'),
]

EVENTOS_GRUPOS_TABELAS = 1
EVENTOS_GRUPOS_NAO_PERIODICOS = 2
EVENTOS_GRUPOS_PERIODICOS = 3

EVENTOS_GRUPOS = [
    (EVENTOS_GRUPOS_TABELAS, '1 - Eventos de Tabelas'),
    (EVENTOS_GRUPOS_NAO_PERIODICOS, '2 - Eventos Não Periódicos'),
    (EVENTOS_GRUPOS_PERIODICOS, '3 - Eventos Periódicos'),
]

ESOCIAL_VERSAO_DEFAULT = 'v_S_01_02_00'
VERSOES = [
    ('v_S_01_00_00', 'Versão S-1.0'),
    ('v_S_01_01_00', 'Versão S-1.1'),
    ('v_S_01_02_00', 'Versão S-1.2'),
    ('v_S_01_03_00', 'Versão S-1.3'),
]

ARQUIVO_FONTE = [
    (0, 'Gerado pelo sistema'),
    (1, 'Importado'),
]

EVENTO_ORIGEM_SISTEMA = 0
EVENTO_ORIGEM_API = 1

EVENTO_ORIGEM = [
    (EVENTO_ORIGEM_SISTEMA, 'Sistema'),
    (EVENTO_ORIGEM_API, 'Api'),
]

EVENTO_COD = {
    's1000': {'codigo': 'evtInfoEmpregador'},
    's1005': {'codigo': 'evtTabEstab'},
    's1010': {'codigo': 'evtTabRubrica'},
    's1020': {'codigo': 'evtTabLotacao'},
    's1070': {'codigo': 'evtTabProcesso'},
}

VERSIONS_CODE = {
    'v_S_01_00_00': [
        's1000', 's1005', 's1010', 's1020', 's1070', ],
    'v_S_01_01_00': [
        's1000', 's1005', 's1010', 's1020', 's1070', ],
    'v_S_01_02_00': [
        's1000', 's1005', 's1010', 's1020', 's1070', ],
    'v_S_01_03_00': [
        's1000', 's1005', 's1010', 's1020', 's1070', ]
}

EVENTOS = [
    ('s1000', 'S-1000 - Informações do Empregador/Contribuinte/Órgão Público'),
    ('s1005', 'S-1005 - Tabela de Estabelecimentos, Obras ou Unidades de Órgãos Públicos'),
    ('s1010', 'S-1010 - Tabela de Rubricas'),
    ('s1020', 'S-1020 - Tabela de Lotações Tributárias'),
    ('s1070', 'S-1070 - Tabela de Processos Administrativos/Judiciais'),
]

SERVICO_ENVIAR = 1
SERVICO_CONSULTAR = 2

SERVICOS = (
    (SERVICO_ENVIAR, 'WsEnviarLoteEventos'),
    (SERVICO_CONSULTAR, 'WsConsultarLoteEventos'),
)

ARQUIVO_TIPO_HEADER = 1
ARQUIVO_TIPO_REQUEST = 2
ARQUIVO_TIPO_RESPONSE = 3

ARQUIVOS_TIPOS = (
    (ARQUIVO_TIPO_HEADER, 'Header'),
    (ARQUIVO_TIPO_REQUEST, 'Request'),
    (ARQUIVO_TIPO_RESPONSE, 'Response'),
)

ESTADOS = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AM', 'Amazonas'),
    ('AP', 'Amapá'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MG', 'Minas Gerais'),
    ('MS', 'Mato Grosso do Sul'),
    ('MT', 'Mato Grosso'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('PR', 'Paraná'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('RS', 'Rio Grande do Sul'),
    ('SC', 'Santa Catarina'),
    ('SE', 'Sergipe'),
    ('SP', 'São Paulo'),
    ('TO', 'Tocantins'),
]

OPERACOES = [
    (1, 'Incluir'),
    (2, 'Alterar'),
    (3, 'Excluir'),
]

SIM_NAO = [
    (0, 'Não'),
    (1, 'Sim'),
]

CHOICES_INSCRICOESTIPOS = [
    (1, '1 - CNPJ'),
    (2, '2 - CPF'),
    (3, '3 - CAEPF (Cadastro de Atividade Econômica de Pessoa Física)'),
    (4, '4 - CNO (Cadastro Nacional de Obra)'),
    (5, '5 - CGC'),
    (6, '6 - CEI'),
]

CHOICES_PROCEMI = [
    (1, '1 - Aplicativo do empregador'),
    (2, '2 - Aplicativo governamental - Empregador Doméstico'),
    (3, '3 - Aplicativo governamental - Web Geral'),
    (4, '4 - Aplicativo governamental - Simplificado Pessoa Jurídica'),
    (5, '5 - Aplicativo governamental - Segurado Especial.'),
]

CHOICES_TPAMB = [
    (1, '1 - Produção'),
    (2, '2 - Produção restrita.'),
]

TPINSC_TRANSMISSOR_EVENTOS = (
    ('1', '1 - CNPJ'),
    ('2', '2 - CPF'),
    ('3', '3 - CAEPF (Cadastro de Atividade Econômica de Pessoa Física)'),
    ('4', '4 - CNO (Cadastro Nacional de Obra)'),
)

TIPO_TRANSMISSOR_EVENTOS = (
    ('', ''),
    ('efdreinf', 'EFD-Reinf'),
)

CODIGO_RESPOSTA = [
    (0, 'Cadastrado'),
    (101, '101 - Lote Aguardando Processamento'),
    (201, '201 - Lote Processado com Sucesso'),
    (202, '202 - Lote Processado com Advertências'),
    (301, '301 - Erro Servidor '),
    (401, '401 - Lote Incorreto - Erro preenchimento'),
    (402, '402 - Lote Incorreto - schema Inválido'),
    (403, '403 - Lote Incorreto - Versão do Schema não permitida'),
    (404, '404 - Lote Incorreto - Erro Certificado'),
    (405, '405 - Lote Incorreto - Lote nulo ou vazio'),
    (501, '501 - Solicitação de Consulta Incorreta - Erro Preenchimento'),
    (502, '502 - Solicitação de Consulta Incorreta - Schema Inválido.'),
    (503, '503 - Solicitação de Consulta Incorreta - Versão do Schema Não Permitida.'),
    (504, '504 - Solicitação de Consulta Incorreta - Erro Certificado.'),
    (505, '505 - Solicitação de Consulta Incorreta - Consulta nula ou vazia.'),
]

CODIGO_STATUS_EFDREINF = [
    (0, '0 - Sucesso'),
    (1, '1 - Erro'),
    (2, '2 - Em Processamento'),
]

IMPORTACAO_STATUS = [
    (0, 'Aguardando'),
    (1, 'Processando'),
    (2, 'Processado com sucesso'),
    (3, 'Erro - Processamento'),
    (4, 'Erro - Outros'),
    (5, 'Erro - Arquivo Inválido'),
    (6, 'Erro - Identidade já existente'),
    (7, 'Erro - Versão de leiaute incompatível'),
    (8, 'Erro - Validação de Leiaute'),
]

TIPO_INSCRICAO = [
    (1, '1 - CNPJ'),
    (2, '2 - CPF'),
]
