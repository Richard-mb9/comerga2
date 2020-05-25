# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='arquivos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('arquivo', models.FileField(upload_to='arquivos_excel')),
            ],
        ),
        migrations.CreateModel(
            name='enderecos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('CEP', models.CharField(max_length=9)),
                ('Estado', models.CharField(max_length=50)),
                ('Cidade', models.CharField(max_length=50)),
                ('bairro', models.CharField(max_length=50)),
                ('Rua', models.CharField(max_length=50)),
                ('numero', models.DecimalField(max_digits=5, decimal_places=0)),
                ('complemento', models.CharField(max_length=50, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lojas',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(verbose_name='Razão Social', max_length=30)),
                ('CNPJ', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('senha', models.CharField(max_length=15)),
                ('confirm', models.CharField(max_length=15)),
                ('DDD_tel', models.IntegerField()),
                ('Telefone', models.CharField(max_length=9)),
                ('DDD_whats', models.IntegerField(blank=True, null=True)),
                ('whatsapp', models.CharField(max_length=10, blank=True, null=True)),
                ('ativa', models.CharField(max_length=4, default='sim')),
                ('CEP', models.CharField(max_length=9)),
                ('Estado', models.CharField(max_length=30)),
                ('Cidade', models.CharField(max_length=30)),
                ('bairro', models.CharField(max_length=30)),
                ('Rua', models.CharField(max_length=50)),
                ('numero', models.DecimalField(max_digits=5, decimal_places=0)),
                ('complemento', models.CharField(max_length=20, blank=True, null=True)),
                ('logomarca', models.ImageField(upload_to='%d')),
            ],
        ),
        migrations.CreateModel(
            name='usuarios',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('Primeiro_nome', models.CharField(verbose_name='Primeiro Nome', max_length=50)),
                ('Ultimo_nome', models.CharField(verbose_name='Ultimo Nome', max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('senha', models.CharField(max_length=12)),
                ('confirm', models.CharField(verbose_name='Confirmação de Senha', max_length=12)),
                ('DDD_tel', models.CharField(max_length=3)),
                ('telefone', models.CharField(max_length=9, blank=True, null=True)),
                ('DDD_cel', models.CharField(max_length=3)),
                ('celular', models.CharField(max_length=10)),
                ('ultimopedido', models.CharField(max_length=15, blank=True, null=True, default='#')),
            ],
        ),
        migrations.AddField(
            model_name='enderecos',
            name='cliente',
            field=models.ForeignKey(to='cadastros.usuarios',on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='arquivos',
            name='cliente',
            field=models.ForeignKey(to='cadastros.Lojas',on_delete=models.CASCADE),
        ),
    ]
