# Generated by Django 3.0.3 on 2020-04-28 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_pedidos_loja'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedidos',
            name='loja',
        ),
    ]
