# Generated by Django 3.0.3 on 2020-05-06 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0014_auto_20200504_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subpedido',
            name='Quantidade',
            field=models.DecimalField(decimal_places=1, max_digits=4),
        ),
    ]
