# Generated by Django 3.0.4 on 2020-04-26 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CEP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CEP', models.CharField(max_length=10)),
                ('Coordenadas', models.CharField(max_length=60)),
            ],
        ),
    ]
