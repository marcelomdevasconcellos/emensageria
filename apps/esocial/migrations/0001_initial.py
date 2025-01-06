# Generated by Django 4.2.17 on 2025-01-03 00:03

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=300, verbose_name='Nome')),
                ('certificado', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/Users/marcelovasconcellos/PycharmProjects/emensageria/certificados/'), upload_to='', verbose_name='Arquivo')),
                ('senha_certificado', models.TextField(blank=True, null=True, verbose_name='Senha do certificado criptografada')),
            ],
            options={
                'verbose_name': 'Certificados',
                'verbose_name_plural': 'Certificados',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Eventos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('identidade', models.CharField(blank=True, max_length=36, null=True, unique=True, verbose_name='Identidade')),
                ('versao', models.CharField(choices=[('v_S_01_00_00', 'Versão S-1.0'), ('v_S_01_01_00', 'Versão S-1.1'), ('v_S_01_02_00', 'Versão S-1.2'), ('v_S_01_03_00', 'Versão S-1.3')], default='v_S_01_03_00', max_length=20, verbose_name='Versão')),
                ('evento', models.CharField(choices=[('s1000', 'S-1000 - Informações do Empregador/Contribuinte/Órgão Público'), ('s1005', 'S-1005 - Tabela de Estabelecimentos, Obras ou Unidades de Órgãos Públicos'), ('s1010', 'S-1010 - Tabela de Rubricas'), ('s1020', 'S-1020 - Tabela de Lotações Tributárias'), ('s1070', 'S-1070 - Tabela de Processos Administrativos/Judiciais'), ('s1200', 'S-1200 - Remuneração de Trabalhador vinculado ao Regime Geral de Previd. Social'), ('s1202', 'S-1202 - Remuneração de Servidor vinculado ao Regime Próprio de Previd. Social'), ('s1207', 'S-1207 - Benefícios - Entes Públicos'), ('s1210', 'S-1210 - Pagamentos de Rendimentos do Trabalho'), ('s1260', 'S-1260 - Comercialização da Produção Rural Pessoa Física'), ('s1270', 'S-1270 - Contratação de Trabalhadores Avulsos Não Portuários'), ('s1280', 'S-1280 - Informações Complementares aos Eventos Periódicos'), ('s1298', 'S-1298 - Reabertura dos Eventos Periódicos'), ('s1299', 'S-1299 - Fechamento dos Eventos Periódicos'), ('s2190', 'S-2190 - Registro Preliminar de Trabalhador'), ('s2200', 'S-2200 - Cadastramento Inicial do Vínculo e Admissão/Ingresso de Trabalhador'), ('s2205', 'S-2205 - Alteração de Dados Cadastrais do Trabalhador'), ('s2206', 'S-2206 - Alteração de Contrato de Trabalho/Relação Estatutária'), ('s2210', 'S-2210 - Comunicação de Acidente de Trabalho'), ('s2220', 'S-2220 - Monitoramento da Saúde do Trabalhador'), ('s2221', 'S-2221 - Exame Toxicológico do Motorista Profissional Empregado'), ('s2230', 'S-2230 - Afastamento Temporário'), ('s2231', 'S-2231 - Cessão/Exercício em Outro Órgão'), ('s2240', 'S-2240 - Condições Ambientais do Trabalho - Agentes Nocivos'), ('s2298', 'S-2298 - Reintegração/Outros Provimentos'), ('s2299', 'S-2299 - Desligamento'), ('s2300', 'S-2300 - Trabalhador Sem Vínculo de Emprego/Estatutário - Início'), ('s2306', 'S-2306 - Trabalhador Sem Vínculo de Emprego/Estatutário - Alteração Contratual'), ('s2399', 'S-2399 - Trabalhador Sem Vínculo de Emprego/Estatutário - Término'), ('s2400', 'S-2400 - Cadastro de Beneficiário - Entes Públicos - Início'), ('s2405', 'S-2405 - Cadastro de Beneficiário - Entes Públicos - Alteração'), ('s2410', 'S-2410 - Cadastro de Benefício - Entes Públicos - Início'), ('s2416', 'S-2416 - Cadastro de Benefício - Entes Públicos - Alteração'), ('s2418', 'S-2418 - Reativação de Benefício - Entes Públicos'), ('s2420', 'S-2420 - Cadastro de Benefício - Entes Públicos - Término'), ('s2500', 'S-2500 - Processo Trabalhista'), ('s2501', 'S-2501 - Informações de Tributos Decorrentes de Processo Trabalhista'), ('s2555', 'S-2555 - Solicitação de Consolidação das Informações de Tributos Decorrentes de Processo Trabalhista'), ('s3000', 'S-3000 - Exclusão de Eventos'), ('s3500', 'S-3500 - Exclusão de Eventos - Processo Trabalhista'), ('s5003', 'S-5003 - Informações do FGTS por Trabalhador'), ('s5013', 'S-5013 - Informações do FGTS Consolidadas por Contribuinte'), ('s5501', 'S-5501 - Informações Consolidadas de Tributos Decorrentes de Processo Trabalhista'), ('s5503', 'S-5503 - Informações do FGTS por Trabalhador em Processo Trabalhista'), ('s8200', 'S-8200 - Anotação Judicial do Vínculo'), ('s8299', 'S-8299 - Baixa Judicial do Vínculo')], max_length=20, verbose_name='Evento')),
                ('operacao', models.IntegerField(blank=True, choices=[(1, 'Incluir'), (2, 'Alterar'), (3, 'Excluir')], null=True, verbose_name='Operações')),
                ('status', models.IntegerField(blank=True, choices=[(-1, 'Importado pela API'), (0, 'Cadastrado (Aguardando validação)'), (1, 'Erro (Aguardando correção)'), (2, 'Validado (Aguardando envio)'), (6, 'Enviando ...'), (3, 'Enviado (Aguardando consulta)'), (7, 'Consultando ...'), (5, 'Consultado')], default=0, verbose_name='Status')),
                ('tpinsc', models.IntegerField(choices=[(1, '1 - CNPJ'), (2, '2 - CPF'), (3, '3 - CAEPF (Cadastro de Atividade Econômica de Pessoa Física)'), (4, '4 - CNO (Cadastro Nacional de Obra)'), (5, '5 - CGC'), (6, '6 - CEI')], verbose_name='Tipo de inscrição')),
                ('nrinsc', models.CharField(help_text='O CNPJ completo somente pode ser utilizado por órgãos públicos, os demais empregadores deverão informar somente o CNPJ base (8 primeiros dígitos do CNPJ)', max_length=15, verbose_name='Número de inscrição')),
                ('tpamb', models.IntegerField(choices=[(1, '1 - Produção'), (2, '2 - Produção restrita.')], default='2', verbose_name='Identificação do ambiente')),
                ('procemi', models.IntegerField(choices=[(1, '1 - Aplicativo do empregador'), (2, '2 - Aplicativo governamental - Empregador Doméstico'), (3, '3 - Aplicativo governamental - Web Geral'), (4, '4 - Aplicativo governamental - Simplificado Pessoa Jurídica'), (5, '5 - Aplicativo governamental - Segurado Especial.')], default='1', verbose_name='Processo de emissão do evento')),
                ('verproc', models.CharField(default='1.8.0', max_length=20, null=True, verbose_name='Versão do processo')),
                ('validacao_precedencia', models.IntegerField(blank=True, choices=[(0, 'Não'), (1, 'Sim')], null=True, verbose_name='Validação de precedência')),
                ('validacoes', models.TextField(blank=True, null=True, verbose_name='Validações')),
                ('arquivo', models.CharField(blank=True, max_length=200, null=True, verbose_name='Arquivo')),
                ('retorno_envio_json', models.JSONField(blank=True, default=dict, null=True, verbose_name='Retorno do envio')),
                ('retorno_consulta_json', models.JSONField(blank=True, default=dict, null=True, verbose_name='Retorno da consulta')),
                ('retorno_envio_lote_json', models.JSONField(blank=True, default=dict, null=True, verbose_name='Retorno do lote do envio')),
                ('retorno_consulta_lote_json', models.JSONField(blank=True, default=dict, null=True, verbose_name='Retorno do lote da consulta')),
                ('evento_json', models.JSONField(blank=True, default=dict, null=True, verbose_name='JSON')),
                ('evento_xml', models.TextField(blank=True, null=True, verbose_name='XML')),
                ('ocorrencias_json', models.JSONField(blank=True, default=dict, null=True, verbose_name='Ocorrências')),
                ('origem', models.IntegerField(choices=[(0, 'Sistema'), (1, 'Api')], default=0, verbose_name='Origem do evento')),
                ('is_aberto', models.BooleanField(default=True, verbose_name='Está aberto para edição')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'ordering': ['versao', 'evento', 'operacao', 'status'],
            },
        ),
        migrations.CreateModel(
            name='EventosHistorico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('identidade', models.CharField(blank=True, max_length=36, null=True, verbose_name='Identidade')),
                ('versao', models.CharField(choices=[('v_S_01_00_00', 'Versão S-1.0'), ('v_S_01_01_00', 'Versão S-1.1'), ('v_S_01_02_00', 'Versão S-1.2'), ('v_S_01_03_00', 'Versão S-1.3')], default='v_S_01_02_00', max_length=20, verbose_name='Versão')),
                ('evento', models.CharField(choices=[('s1000', 'S-1000 - Informações do Empregador/Contribuinte/Órgão Público'), ('s1005', 'S-1005 - Tabela de Estabelecimentos, Obras ou Unidades de Órgãos Públicos'), ('s1010', 'S-1010 - Tabela de Rubricas'), ('s1020', 'S-1020 - Tabela de Lotações Tributárias'), ('s1070', 'S-1070 - Tabela de Processos Administrativos/Judiciais'), ('s1200', 'S-1200 - Remuneração de Trabalhador vinculado ao Regime Geral de Previd. Social'), ('s1202', 'S-1202 - Remuneração de Servidor vinculado ao Regime Próprio de Previd. Social'), ('s1207', 'S-1207 - Benefícios - Entes Públicos'), ('s1210', 'S-1210 - Pagamentos de Rendimentos do Trabalho'), ('s1260', 'S-1260 - Comercialização da Produção Rural Pessoa Física'), ('s1270', 'S-1270 - Contratação de Trabalhadores Avulsos Não Portuários'), ('s1280', 'S-1280 - Informações Complementares aos Eventos Periódicos'), ('s1298', 'S-1298 - Reabertura dos Eventos Periódicos'), ('s1299', 'S-1299 - Fechamento dos Eventos Periódicos'), ('s2190', 'S-2190 - Registro Preliminar de Trabalhador'), ('s2200', 'S-2200 - Cadastramento Inicial do Vínculo e Admissão/Ingresso de Trabalhador'), ('s2205', 'S-2205 - Alteração de Dados Cadastrais do Trabalhador'), ('s2206', 'S-2206 - Alteração de Contrato de Trabalho/Relação Estatutária'), ('s2210', 'S-2210 - Comunicação de Acidente de Trabalho'), ('s2220', 'S-2220 - Monitoramento da Saúde do Trabalhador'), ('s2221', 'S-2221 - Exame Toxicológico do Motorista Profissional Empregado'), ('s2230', 'S-2230 - Afastamento Temporário'), ('s2231', 'S-2231 - Cessão/Exercício em Outro Órgão'), ('s2240', 'S-2240 - Condições Ambientais do Trabalho - Agentes Nocivos'), ('s2298', 'S-2298 - Reintegração/Outros Provimentos'), ('s2299', 'S-2299 - Desligamento'), ('s2300', 'S-2300 - Trabalhador Sem Vínculo de Emprego/Estatutário - Início'), ('s2306', 'S-2306 - Trabalhador Sem Vínculo de Emprego/Estatutário - Alteração Contratual'), ('s2399', 'S-2399 - Trabalhador Sem Vínculo de Emprego/Estatutário - Término'), ('s2400', 'S-2400 - Cadastro de Beneficiário - Entes Públicos - Início'), ('s2405', 'S-2405 - Cadastro de Beneficiário - Entes Públicos - Alteração'), ('s2410', 'S-2410 - Cadastro de Benefício - Entes Públicos - Início'), ('s2416', 'S-2416 - Cadastro de Benefício - Entes Públicos - Alteração'), ('s2418', 'S-2418 - Reativação de Benefício - Entes Públicos'), ('s2420', 'S-2420 - Cadastro de Benefício - Entes Públicos - Término'), ('s2500', 'S-2500 - Processo Trabalhista'), ('s2501', 'S-2501 - Informações de Tributos Decorrentes de Processo Trabalhista'), ('s2555', 'S-2555 - Solicitação de Consolidação das Informações de Tributos Decorrentes de Processo Trabalhista'), ('s3000', 'S-3000 - Exclusão de Eventos'), ('s3500', 'S-3500 - Exclusão de Eventos - Processo Trabalhista'), ('s5003', 'S-5003 - Informações do FGTS por Trabalhador'), ('s5013', 'S-5013 - Informações do FGTS Consolidadas por Contribuinte'), ('s5501', 'S-5501 - Informações Consolidadas de Tributos Decorrentes de Processo Trabalhista'), ('s5503', 'S-5503 - Informações do FGTS por Trabalhador em Processo Trabalhista'), ('s8200', 'S-8200 - Anotação Judicial do Vínculo'), ('s8299', 'S-8299 - Baixa Judicial do Vínculo')], max_length=20, verbose_name='Evento')),
                ('operacao', models.IntegerField(blank=True, choices=[(1, 'Incluir'), (2, 'Alterar'), (3, 'Excluir')], null=True, verbose_name='Operações')),
                ('status', models.IntegerField(blank=True, choices=[(-1, 'Importado pela API'), (0, 'Cadastrado (Aguardando validação)'), (1, 'Erro (Aguardando correção)'), (2, 'Validado (Aguardando envio)'), (6, 'Enviando ...'), (3, 'Enviado (Aguardando consulta)'), (7, 'Consultando ...'), (5, 'Consultado')], default=0, verbose_name='Status')),
                ('tpinsc', models.IntegerField(choices=[(1, '1 - CNPJ'), (2, '2 - CPF'), (3, '3 - CAEPF (Cadastro de Atividade Econômica de Pessoa Física)'), (4, '4 - CNO (Cadastro Nacional de Obra)'), (5, '5 - CGC'), (6, '6 - CEI')], verbose_name='Tipo de inscrição')),
                ('nrinsc', models.CharField(max_length=15, verbose_name='Numero de inscrição')),
                ('tpamb', models.IntegerField(choices=[(1, '1 - Produção'), (2, '2 - Produção restrita.')], null=True, verbose_name='Identificação do ambiente')),
                ('procemi', models.IntegerField(choices=[(1, '1 - Aplicativo do empregador'), (2, '2 - Aplicativo governamental - Empregador Doméstico'), (3, '3 - Aplicativo governamental - Web Geral'), (4, '4 - Aplicativo governamental - Simplificado Pessoa Jurídica'), (5, '5 - Aplicativo governamental - Segurado Especial.')], default=1, null=True, verbose_name='Processo de emissão do evento')),
                ('verproc', models.CharField(max_length=20, null=True, verbose_name='Versão do processo')),
                ('validacao_precedencia', models.IntegerField(blank=True, choices=[(0, 'Não'), (1, 'Sim')], null=True, verbose_name='Validação de precedência')),
                ('validacoes', models.TextField(blank=True, null=True, verbose_name='Validações')),
                ('arquivo', models.CharField(blank=True, max_length=200, null=True, verbose_name='Arquivo')),
                ('retorno_envio_json', models.JSONField(blank=True, default=dict, null=True, verbose_name='Retorno do envio')),
                ('retorno_consulta_json', models.JSONField(blank=True, default=dict, null=True, verbose_name='Retorno da consulta')),
                ('retorno_envio_lote_json', models.JSONField(blank=True, default=dict, null=True, verbose_name='Retorno do lote do envio')),
                ('retorno_consulta_lote_json', models.JSONField(blank=True, default=dict, null=True, verbose_name='Retorno do lote da consulta')),
                ('evento_json', models.JSONField(blank=True, default=dict, null=True, verbose_name='JSON')),
                ('evento_xml', models.TextField(blank=True, null=True, verbose_name='XML')),
                ('ocorrencias_json', models.JSONField(blank=True, default=dict, null=True, verbose_name='Ocorrências')),
                ('origem', models.IntegerField(choices=[(0, 'Sistema'), (1, 'Api')], default=0, verbose_name='Origem do evento')),
                ('is_aberto', models.BooleanField(default=True, verbose_name='Está aberto para edição')),
            ],
            options={
                'verbose_name': 'Histórico do Evento',
                'verbose_name_plural': 'Histórico dos Eventos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Lotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('empregador_tpinsc', models.IntegerField(choices=[(1, '1 - CNPJ'), (2, '2 - CPF')], verbose_name='Tipo de inscrição do empregador')),
                ('empregador_nrinsc', models.CharField(max_length=15, verbose_name='Número de inscrição do empregador')),
                ('grupo', models.IntegerField(choices=[(1, '1 - Eventos de Tabelas'), (2, '2 - Eventos Não Periódicos'), (3, '3 - Eventos Periódicos')], verbose_name='Grupo')),
                ('status', models.IntegerField(blank=True, choices=[(0, 'Cadastrado'), (1, 'Aguardando envio'), (2, 'Enviando ...'), (3, 'Enviado'), (4, 'Erro no envio'), (5, 'Consultando ...'), (6, 'Consultado'), (7, 'Erro na consulta')], default=0, verbose_name='Status')),
                ('resposta_codigo', models.CharField(blank=True, max_length=10, null=True, verbose_name='Código da Resposta')),
                ('resposta_descricao', models.TextField(blank=True, null=True, verbose_name='Descrição da resposta')),
                ('data_hora_envio', models.DateTimeField(blank=True, null=True, verbose_name='Data/Hora do envio')),
                ('data_hora_consulta', models.DateTimeField(blank=True, null=True, verbose_name='Data/Hora da consulta')),
                ('recepcao_data_hora', models.DateTimeField(blank=True, null=True, verbose_name='Data/Hora da recepção')),
                ('recepcao_versao_aplicativo', models.CharField(blank=True, max_length=50, null=True, verbose_name='Versão do aplicativo de recepção')),
                ('protocolo', models.CharField(blank=True, max_length=50, null=True, verbose_name='Protocolo')),
                ('processamento_versao_aplicativo', models.CharField(blank=True, max_length=50, null=True, verbose_name='Versão do aplicativo de processamento')),
                ('tempo_estimado_conclusao', models.IntegerField(blank=True, null=True, verbose_name='Tempo estimado de conclusão')),
                ('arquivo_header', models.CharField(blank=True, max_length=200, null=True, verbose_name='Arquivo header')),
                ('arquivo_request', models.CharField(blank=True, max_length=200, null=True, verbose_name='Arquivo request')),
                ('arquivo_response', models.CharField(blank=True, max_length=200, null=True, verbose_name='Arquivo response')),
                ('retorno_envio_json', models.JSONField(blank=True, null=True, verbose_name='Retorno do envio')),
                ('retorno_consulta_json', models.JSONField(blank=True, null=True, verbose_name='Retorno da consulta')),
                ('ocorrencias_json', models.JSONField(blank=True, null=True, verbose_name='Ocorrências')),
                ('batch_xml', models.TextField(blank=True, null=True, verbose_name='Lote (XML)')),
                ('response_send_xml', models.TextField(blank=True, null=True, verbose_name='Retorno do envio (XML)')),
                ('response_retrieve_xml', models.TextField(blank=True, null=True, verbose_name='Retorno da consulta (XML)')),
            ],
            options={
                'verbose_name': 'Lote',
                'verbose_name_plural': 'Lotes',
            },
        ),
        migrations.CreateModel(
            name='Transmissor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('transmissor_tpinsc', models.IntegerField(choices=[(1, '1 - CNPJ'), (2, '2 - CPF')], verbose_name='Tipo de inscrição do transmissor')),
                ('transmissor_nrinsc', models.CharField(max_length=15, verbose_name='Número de inscrição do transmissor')),
                ('nome_empresa', models.CharField(max_length=200, unique=True, verbose_name='Nome da empresa')),
                ('logotipo', models.FileField(blank=True, null=True, upload_to='logotipo', verbose_name='Logotipo')),
                ('endereco_completo', models.TextField(blank=True, null=True, verbose_name='Endereço')),
                ('tpinsc', models.IntegerField(choices=[(1, '1 - CNPJ'), (2, '2 - CPF')], verbose_name='Tipo de inscrição do empregador')),
                ('nrinsc', models.CharField(help_text='O CNPJ completo somente pode ser utilizado por órgãos públicos, os demais empregadores deverão informar somente o CNPJ base (8 primeiros dígitos do CNPJ)', max_length=15, unique=True, verbose_name='Número de inscrição do empregador')),
                ('certificado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_certificado', to='esocial.certificados', verbose_name='Certificado')),
            ],
            options={
                'verbose_name': 'Transmissor',
                'verbose_name_plural': 'Transmissor',
            },
        ),
    ]
