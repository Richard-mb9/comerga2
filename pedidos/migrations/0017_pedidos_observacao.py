# Generated by Django 3.0.4 on 2020-05-19 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0016_pedidos_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='observacao',
            field=models.CharField(default='', max_length=150, verbose_name='Observação'),
        ),
    ]
