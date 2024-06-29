# Generated by Django 3.2.4 on 2021-06-27 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esocial', '0017_auto_20210627_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventos',
            name='procemi',
            field=models.IntegerField(choices=[(1, '1 - Aplicativo do empregador'), (2, '2 - Aplicativo governamental - Empregador Doméstico'), (3, '3 - Aplicativo governamental - Web Geral'), (4, '4 - Aplicativo governamental - Simplificado Pessoa Jurídica'), (5, '5 - Aplicativo governamental - Segurado Especial.')], default='1', verbose_name='Processo de emissão do evento'),
        ),
        migrations.AlterField(
            model_name='eventos',
            name='status',
            field=models.IntegerField(blank=True, choices=[(-1, 'Importado pela API'), (0, 'Cadastrado (Aguardando validação)'), (1, 'Erro (Aguardando correção)'), (2, 'Validado (Aguardando envio)'), (3, 'Enviado (Aguardando consulta)'), (5, 'Consultado')], default=0, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='eventos',
            name='tpamb',
            field=models.IntegerField(choices=[(1, '1 - Produção'), (2, '2 - Produção restrita.')], default='2', verbose_name='Identificação do ambiente'),
        ),
        migrations.AlterField(
            model_name='eventos',
            name='verproc',
            field=models.CharField(default='1.0.0', max_length=20, null=True, verbose_name='Versão do processo'),
        ),
        migrations.AlterField(
            model_name='eventoshistorico',
            name='status',
            field=models.IntegerField(blank=True, choices=[(-1, 'Importado pela API'), (0, 'Cadastrado (Aguardando validação)'), (1, 'Erro (Aguardando correção)'), (2, 'Validado (Aguardando envio)'), (3, 'Enviado (Aguardando consulta)'), (5, 'Consultado')], default=0, verbose_name='Status'),
        ),
    ]
