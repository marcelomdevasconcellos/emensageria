# Generated by Django 3.2.4 on 2021-06-20 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('esocial', '0009_auto_20210616_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventos',
            name='certificado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='certificado_esocial', to='esocial.certificados', verbose_name='Certificado'),
        ),
        migrations.AlterField(
            model_name='eventos',
            name='nrinsc',
            field=models.CharField(help_text='O CNPJ completo somente pode ser utilizado por órgãos públicos, os demais empregadores deverão informar somente o CNPJ base (8 primeiros dígitos do CNPJ)', max_length=15, verbose_name='Número de inscrição'),
        ),
        migrations.AlterField(
            model_name='transmissor',
            name='nrinsc',
            field=models.CharField(help_text='O CNPJ completo somente pode ser utilizado por órgãos públicos, os demais empregadores deverão informar somente o CNPJ base (8 primeiros dígitos do CNPJ)', max_length=15, unique=True, verbose_name='Número de inscrição do empregador'),
        ),
    ]
