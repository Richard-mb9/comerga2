# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0002_auto_20200424_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='lojas',
            name='distancia',
            field=models.DecimalField(verbose_name='Distancia para entregas', default=5, max_digits=5, decimal_places=0),
        ),
        migrations.AddField(
            model_name='lojas',
            name='latitude',
            field=models.CharField(max_length=20, default=''),
        ),
        migrations.AddField(
            model_name='lojas',
            name='longitude',
            field=models.CharField(max_length=20, default=''),
        ),
    ]
