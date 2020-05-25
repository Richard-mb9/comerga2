# Generated by Django 3.0.3 on 2020-04-29 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordenadas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cep',
            name='Cidade',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cep',
            name='Estado',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='cep',
            name='Rua',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cep',
            name='complemento',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='cep',
            name='numero',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
