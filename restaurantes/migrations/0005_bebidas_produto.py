# Generated by Django 3.0.3 on 2020-05-20 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0005_auto_20200506_1451'),
        ('restaurantes', '0004_auto_20200520_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='bebidas',
            name='produto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='produtos.Produtos'),
        ),
    ]
