# Generated by Django 4.2.17 on 2025-01-03 00:03

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(error_messages={'unique': 'Um usuário com este CPF já está cadastrado no sistema.'}, help_text='Obrigatório. Informe o CPF do usuário.', max_length=14, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='CPF')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Nome Completo')),
                ('eventos', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('s1000', 'S-1000 - Informações do Empregador/Contribuinte/Órgão Público'), ('s1005', 'S-1005 - Tabela de Estabelecimentos, Obras ou Unidades de Órgãos Públicos'), ('s1010', 'S-1010 - Tabela de Rubricas'), ('s1020', 'S-1020 - Tabela de Lotações Tributárias'), ('s1070', 'S-1070 - Tabela de Processos Administrativos/Judiciais'), ('s1200', 'S-1200 - Remuneração de Trabalhador vinculado ao Regime Geral de Previd. Social'), ('s1202', 'S-1202 - Remuneração de Servidor vinculado ao Regime Próprio de Previd. Social'), ('s1207', 'S-1207 - Benefícios - Entes Públicos'), ('s1210', 'S-1210 - Pagamentos de Rendimentos do Trabalho'), ('s1260', 'S-1260 - Comercialização da Produção Rural Pessoa Física'), ('s1270', 'S-1270 - Contratação de Trabalhadores Avulsos Não Portuários'), ('s1280', 'S-1280 - Informações Complementares aos Eventos Periódicos'), ('s1298', 'S-1298 - Reabertura dos Eventos Periódicos'), ('s1299', 'S-1299 - Fechamento dos Eventos Periódicos'), ('s2190', 'S-2190 - Registro Preliminar de Trabalhador'), ('s2200', 'S-2200 - Cadastramento Inicial do Vínculo e Admissão/Ingresso de Trabalhador'), ('s2205', 'S-2205 - Alteração de Dados Cadastrais do Trabalhador'), ('s2206', 'S-2206 - Alteração de Contrato de Trabalho/Relação Estatutária'), ('s2210', 'S-2210 - Comunicação de Acidente de Trabalho'), ('s2220', 'S-2220 - Monitoramento da Saúde do Trabalhador'), ('s2221', 'S-2221 - Exame Toxicológico do Motorista Profissional Empregado'), ('s2230', 'S-2230 - Afastamento Temporário'), ('s2231', 'S-2231 - Cessão/Exercício em Outro Órgão'), ('s2240', 'S-2240 - Condições Ambientais do Trabalho - Agentes Nocivos'), ('s2298', 'S-2298 - Reintegração/Outros Provimentos'), ('s2299', 'S-2299 - Desligamento'), ('s2300', 'S-2300 - Trabalhador Sem Vínculo de Emprego/Estatutário - Início'), ('s2306', 'S-2306 - Trabalhador Sem Vínculo de Emprego/Estatutário - Alteração Contratual'), ('s2399', 'S-2399 - Trabalhador Sem Vínculo de Emprego/Estatutário - Término'), ('s2400', 'S-2400 - Cadastro de Beneficiário - Entes Públicos - Início'), ('s2405', 'S-2405 - Cadastro de Beneficiário - Entes Públicos - Alteração'), ('s2410', 'S-2410 - Cadastro de Benefício - Entes Públicos - Início'), ('s2416', 'S-2416 - Cadastro de Benefício - Entes Públicos - Alteração'), ('s2418', 'S-2418 - Reativação de Benefício - Entes Públicos'), ('s2420', 'S-2420 - Cadastro de Benefício - Entes Públicos - Término'), ('s2500', 'S-2500 - Processo Trabalhista'), ('s2501', 'S-2501 - Informações de Tributos Decorrentes de Processo Trabalhista'), ('s2555', 'S-2555 - Solicitação de Consolidação das Informações de Tributos Decorrentes de Processo Trabalhista'), ('s3000', 'S-3000 - Exclusão de Eventos'), ('s3500', 'S-3500 - Exclusão de Eventos - Processo Trabalhista'), ('s5003', 'S-5003 - Informações do FGTS por Trabalhador'), ('s5013', 'S-5013 - Informações do FGTS Consolidadas por Contribuinte'), ('s5501', 'S-5501 - Informações Consolidadas de Tributos Decorrentes de Processo Trabalhista'), ('s5503', 'S-5503 - Informações do FGTS por Trabalhador em Processo Trabalhista'), ('s8200', 'S-8200 - Anotação Judicial do Vínculo'), ('s8299', 'S-8299 - Baixa Judicial do Vínculo')], max_length=275, null=True, verbose_name='Eventos')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='Acessa o sistema?')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='Está ativo?')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='É administrador?')),
                ('user_str', models.CharField(blank=True, max_length=200, null=True, verbose_name='User String')),
                ('user_search_str', models.CharField(blank=True, max_length=200, null=True, verbose_name='User Search String')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='Grupos')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
