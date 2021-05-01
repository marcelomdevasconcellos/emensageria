URLS_ESOCIAL = {
    # 'Produção': {
    #     'WsEnviarLoteEventos': {
    #         'url': 'https://webservices.producaorestrita.esocial.gov.br/servicos/empregador/enviarloteeventos/WsEnviarLoteEventos.svc',
    #         'action': 'http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/v1_1_0/ServicoEnviarLoteEventos/EnviarLoteEventos',
    #     },
    #     'WsConsultarLoteEventos': {
    #         'url': 'https://webservices.producaorestrita.esocial.gov.br/servicos/empregador/consultarloteeventos/WsConsultarLoteEventos.svc',
    #         'action': 'http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/consulta/retornoProcessamento/v1_1_0/ServicoConsultarLoteEventos/ConsultarLoteEventos',
    #     },
    # },
    'Produção-Restrita': {
        'WsEnviarLoteEventos': {
            'url': 'https://webservices.producaorestrita.esocial.gov.br/servicos/empregador/enviarloteeventos/WsEnviarLoteEventos.svc',
            'action': 'http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/v1_1_0/ServicoEnviarLoteEventos/EnviarLoteEventos',
        },
        'WsConsultarLoteEventos': {
            'url': 'https://webservices.producaorestrita.esocial.gov.br/servicos/empregador/consultarloteeventos/WsConsultarLoteEventos.svc',
            'action': 'http://www.esocial.gov.br/servicos/empregador/lote/eventos/envio/consulta/retornoProcessamento/v1_1_0/ServicoConsultarLoteEventos/ConsultarLoteEventos',
        },
    },
}

STATUS_EVENTO_CADASTRADO = 0
STATUS_EVENTO_IMPORTADO = 1
STATUS_EVENTO_DUPLICADO = 2
STATUS_EVENTO_GERADO = 3
STATUS_EVENTO_GERADO_ERRO = 4
STATUS_EVENTO_ASSINADO = 5
STATUS_EVENTO_ASSINADO_ERRO = 6
STATUS_EVENTO_VALIDADO = 7
STATUS_EVENTO_VALIDADO_ERRO = 8
STATUS_EVENTO_AGUARD_PRECEDENCIA = 9
STATUS_EVENTO_AGUARD_ENVIO = 10
STATUS_EVENTO_ENVIADO = 11
STATUS_EVENTO_ENVIADO_ERRO = 12
STATUS_EVENTO_PROCESSADO = 13


EVENTO_STATUS = [
    (STATUS_EVENTO_CADASTRADO, 'Cadastrado'),
    (STATUS_EVENTO_IMPORTADO, 'Importado'),
    (STATUS_EVENTO_DUPLICADO, 'Duplicado'),
    (STATUS_EVENTO_GERADO, 'Gerado'),
    (STATUS_EVENTO_GERADO_ERRO, 'Erro na Geração'),
    (STATUS_EVENTO_GERADO_ERRO, 'Assinado'),
    (STATUS_EVENTO_ASSINADO_ERRO, 'Erro na Assinatura'),
    (STATUS_EVENTO_VALIDADO, 'Validado'),
    (STATUS_EVENTO_VALIDADO_ERRO, 'Erro na validação'),
    (STATUS_EVENTO_AGUARD_PRECEDENCIA, 'Aguardando envio de precedência'),
    (STATUS_EVENTO_AGUARD_ENVIO, 'Aguardando envio'),
    (STATUS_EVENTO_ENVIADO, 'Enviado'),
    (STATUS_EVENTO_ENVIADO_ERRO, 'Erro no Envio/Consulta'),
    (STATUS_EVENTO_PROCESSADO, 'Processado'),
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


VERSOES = [
    ('v2_05_00', 'Versão 2.05.00'),
]

EVENTO_COD = {
    's1000': {'codigo': 'evtInfoEmpregador' },
    's1005': {'codigo': 'evtTabEstab' },
    's1010': {'codigo': 'evtTabRubrica' },
    's1020': {'codigo': 'evtTabLotacao' },
    's1030': {'codigo': 'evtTabCargo' },
    's1035': {'codigo': 'evtTabCarreira' },
    's1040': {'codigo': 'evtTabFuncao' },
    's1050': {'codigo': 'evtTabHorTur' },
    's1060': {'codigo': 'evtTabAmbiente' },
    's1070': {'codigo': 'evtTabProcesso' },
    's1080': {'codigo': 'evtTabOperPort' },
    's1200': {'codigo': 'evtRemun' },
    's1202': {'codigo': 'evtRmnRPPS' },
    's1207': {'codigo': 'evtBenPrRP' },
    's1210': {'codigo': 'evtPgtos' },
    's1250': {'codigo': 'evtAqProd' },
    's1260': {'codigo': 'evtComProd' },
    's1270': {'codigo': 'evtContratAvNP' },
    's1280': {'codigo': 'evtInfoComplPer' },
    's1295': {'codigo': 'evtTotConting' },
    's1298': {'codigo': 'evtReabreEvPer' },
    's1299': {'codigo': 'evtFechaEvPer' },
    's1300': {'codigo': 'evtContrSindPatr' },
    's2190': {'codigo': 'evtAdmPrelim' },
    's2200': {'codigo': 'evtAdmissao' },
    's2205': {'codigo': 'evtAltCadastral' },
    's2206': {'codigo': 'evtAltContratual' },
    's2210': {'codigo': 'evtCAT' },
    's2220': {'codigo': 'evtMonit' },
    's2221': {'codigo': 'evtToxic' },
    's2230': {'codigo': 'evtAfastTemp' },
    's2240': {'codigo': 'evtExpRisco' },
    's2245': {'codigo': 'evtTreiCap' },
    's2250': {'codigo': 'evtAvPrevio' },
    's2260': {'codigo': 'evtConvInterm' },
    's2298': {'codigo': 'evtReintegr' },
    's2299': {'codigo': 'evtDeslig' },
    's2300': {'codigo': 'evtTSVInicio' },
    's2306': {'codigo': 'evtTSVAltContr' },
    's2399': {'codigo': 'evtTSVTermino' },
    's2400': {'codigo': 'evtCdBenPrRP' },
    's3000': {'codigo': 'evtExclusao' },
}


EVENTOS = [
    ('s1000', 'S-1000 - Informações do Empregador/Contribuinte/Órgão Público'),
    ('s1005', 'S-1005 - Tabela de Estabelecimentos, Obras ou Unidades de Órgãos Públicos'),
    ('s1010', 'S-1010 - Tabela de Rubricas'),
    ('s1020', 'S-1020 - Tabela de Lotações Tributárias'),
    ('s1030', 'S-1030 - Tabela de Cargos/Empregos Públicos'),
    ('s1035', 'S-1035 - Tabela de Carreiras Públicas'),
    ('s1040', 'S-1040 - Tabela de Funções/Cargos em Comissão'),
    ('s1050', 'S-1050 - Tabela de Horários/Turnos de Trabalho'),
    ('s1060', 'S-1060 - Tabela de Ambientes de Trabalho'),
    ('s1070', 'S-1070 - Tabela de Processos Administrativos/Judiciais'),
    ('s1080', 'S-1080 - Tabela de Operadores Portuários'),
    ('s1200', 'S-1200 - Remuneração de trabalhador vinculado ao Regime Geral de Previd. Social'),
    ('s1202', 'S-1202 - Remuneração de servidor vinculado a Regime Próprio de Previd. Social'),
    ('s1207', 'S-1207 - Benefícios previdenciários - RPPS'),
    ('s1210', 'S-1210 - Pagamentos de Rendimentos do Trabalho'),
    ('s1250', 'S-1250 - Aquisição de Produção Rural'),
    ('s1260', 'S-1260 - Comercialização da Produção Rural Pessoa Física'),
    ('s1270', 'S-1270 - Contratação de Trabalhadores Avulsos Não Portuários'),
    ('s1280', 'S-1280 - Informações Complementares aos Eventos Periódicos'),
    ('s1295', 'S-1295 - Solicitação de Totalização para Pagamento em Contingência'),
    ('s1298', 'S-1298 - Reabertura dos Eventos Periódicos'),
    ('s1299', 'S-1299 - Fechamento dos Eventos Periódicos'),
    ('s1300', 'S-1300 - Contribuição Sindical Patronal'),
    ('s2190', 'S-2190 - Admissão de Trabalhador - Registro Preliminar'),
    ('s2200', 'S-2200 - Cadastramento Inicial do Vínculo e Admissão/Ingresso de Trabalhador'),
    ('s2205', 'S-2205 - Alteração de Dados Cadastrais do Trabalhador'),
    ('s2206', 'S-2206 - Alteração de Contrato de Trabalho'),
    ('s2210', 'S-2210 - Comunicação de Acidente de Trabalho'),
    ('s2220', 'S-2220 - Monitoramento da Saúde do Trabalhador'),
    ('s2221', 'S-2221 - Exame Toxicológico do Motorista Profissional'),
    ('s2230', 'S-2230 - Afastamento Temporário'),
    ('s2240', 'S-2240 - Condições Ambientais do Trabalho - Fatores de Risco'),
    ('s2245', 'S-2245 - Treinamentos, Capacitações, Exercícios Simulados e Outras Anotações'),
    ('s2250', 'S-2250 - Aviso Prévio'),
    ('s2260', 'S-2260 - Convocação para Trabalho Intermitente'),
    ('s2298', 'S-2298 - Reintegração'),
    ('s2299', 'S-2299 - Desligamento'),
    ('s2300', 'S-2300 - Trabalhador Sem Vínculo de Emprego/Estatutário - Início'),
    ('s2306', 'S-2306 - Trabalhador Sem Vínculo de Emprego/Estatutário - Alteração Contratual'),
    ('s2399', 'S-2399 - Trabalhador Sem Vínculo de Emprego/Estatutário - Término'),
    ('s2400', 'S-2400 - Cadastro de Benefícios Previdenciários - RPPS'),
    ('s3000', 'S-3000 - Exclusão de eventos'),
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
    (3, '3 - CAEPF (Cadastro de Atividade Econômica de Pessoa Física)'),
    (4, '4 - CNO (Cadastro Nacional de Obra)'),
]
