# Generated by Django 3.0.6 on 2020-05-28 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordenadas', '0003_auto_20200429_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='solicitacoes_geo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=12)),
                ('hora', models.CharField(max_length=9)),
                ('ender', models.CharField(max_length=100)),
            ],
        ),
    ]
