# Generated by Django 3.2.4 on 2021-06-20 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('esocial', '0010_auto_20210620_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventoshistorico',
            name='certificado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='certificado_esocial_historico', to='esocial.certificados', verbose_name='Certificado'),
        ),
    ]