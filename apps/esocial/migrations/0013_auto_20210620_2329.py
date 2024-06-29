# Generated by Django 3.2.4 on 2021-06-20 23:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('esocial', '0012_transmissor_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificados',
            name='users',
            field=models.ManyToManyField(help_text='Informe a lista de usuários que tem acesso a utilizar este certificado', related_name='certificado_users', to=settings.AUTH_USER_MODEL, verbose_name='Usuários'),
        ),
        migrations.AlterField(
            model_name='transmissor',
            name='users',
            field=models.ManyToManyField(help_text='Informe a lista de usuários que tem acesso a utilizar este transmissor', related_name='transmissores_users', to=settings.AUTH_USER_MODEL, verbose_name='Usuários'),
        ),
    ]
