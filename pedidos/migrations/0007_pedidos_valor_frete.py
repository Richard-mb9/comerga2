# Generated by Django 3.0.3 on 2020-04-29 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0006_auto_20200429_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='valor_frete',
            field=models.IntegerField(default=0),
        ),
    ]
