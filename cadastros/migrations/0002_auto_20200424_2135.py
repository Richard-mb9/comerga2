# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enderecos',
            name='latitude',
            field=models.CharField(max_length=20, default=''),
        ),
        migrations.AddField(
            model_name='enderecos',
            name='longitude',
            field=models.CharField(max_length=20, default=''),
        ),
    ]
