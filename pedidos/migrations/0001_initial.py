# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0001_initial'),
        ('cadastros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='pedidos',
            fields=[
                ('pedido', models.AutoField(primary_key=True, serialize=False)),
                ('total', models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)),
                ('pedidofechado', models.CharField(max_length=5, null=True, default='não')),
                ('status_entrega', models.CharField(max_length=15, default='não entrege')),
                ('status_pagamento', models.CharField(max_length=10, default='não pago')),
                ('cliente', models.ForeignKey(to='cadastros.usuarios',on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='SubPedido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Quantidade', models.IntegerField()),
                ('total', models.DecimalField(blank=True, null=True, max_digits=7, decimal_places=2)),
                ('item', models.ForeignKey(to='produtos.Produtos',on_delete=models.CASCADE)),
                ('loja', models.ForeignKey(to='cadastros.Lojas',on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='pedidos',
            name='itens',
            field=models.ManyToManyField(blank=True, to='pedidos.SubPedido'),
        ),
    ]
