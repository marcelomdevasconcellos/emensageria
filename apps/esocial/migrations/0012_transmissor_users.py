# Generated by Django 3.2.4 on 2021-06-20 23:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('esocial', '0011_eventoshistorico_certificado'),
    ]

    operations = [
        migrations.AddField(
            model_name='transmissor',
            name='users',
            field=models.ManyToManyField(related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='Usuários'),
        ),
    ]
