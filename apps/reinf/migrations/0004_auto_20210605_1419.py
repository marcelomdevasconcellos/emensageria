# Generated by Django 3.2 on 2021-06-05 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reinf', '0003_auto_20210605_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventos',
            name='evento_json',
            field=models.TextField(blank=True, null=True, verbose_name='JSON'),
        ),
        migrations.AlterField(
            model_name='eventos',
            name='ocorrencias_json',
            field=models.TextField(blank=True, null=True, verbose_name='Ocorrências'),
        ),
    ]