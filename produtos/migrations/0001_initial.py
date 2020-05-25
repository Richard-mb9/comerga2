# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('codigo_de_barras', models.DecimalField(default=0, max_digits=13, decimal_places=0)),
                ('nome', models.CharField(max_length=50)),
                ('valor', models.DecimalField(max_digits=7, decimal_places=2)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='produtos')),
                ('id_loja', models.ForeignKey(to='cadastros.Lojas',on_delete=models.CASCADE)),
            ],
        ),
    ]
