# Generated by Django 3.2 on 2024-10-11 20:15

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esocial', '0027_auto_20240509_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificados',
            name='certificado',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/Users/marcelovasconcellos/PycharmProjects/emensageria/certificados/'), upload_to='', verbose_name='Arquivo'),
        ),
        migrations.AlterField(
            model_name='eventos',
            name='verproc',
            field=models.CharField(default='1.8.0', max_length=20, null=True, verbose_name='Versão do processo'),
        ),
        migrations.AlterField(
            model_name='eventos',
            name='versao',
            field=models.CharField(choices=[('v_S_01_00_00', 'Versão S-1.0'), ('v_S_01_01_00', 'Versão S-1.1'), ('v_S_01_02_00', 'Versão S-1.2'), ('v_S_01_03_00', 'Versão S-1.3')], default='v_S_01_02_00', max_length=20, verbose_name='Versão'),
        ),
        migrations.AlterField(
            model_name='eventoshistorico',
            name='versao',
            field=models.CharField(choices=[('v_S_01_00_00', 'Versão S-1.0'), ('v_S_01_01_00', 'Versão S-1.1'), ('v_S_01_02_00', 'Versão S-1.2'), ('v_S_01_03_00', 'Versão S-1.3')], default='v_S_01_02_00', max_length=20, verbose_name='Versão'),
        ),
    ]
