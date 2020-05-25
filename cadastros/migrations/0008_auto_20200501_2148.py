# Generated by Django 3.0.3 on 2020-05-02 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0007_auto_20200430_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='lojas',
            name='valor_minimo_compra',
            field=models.DecimalField(decimal_places=2, default=50, max_digits=6),
        ),
        migrations.AddField(
            model_name='lojas',
            name='valor_minimo_frete',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
