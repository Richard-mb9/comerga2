# Generated by Django 3.0.3 on 2020-05-11 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transferencias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferencias',
            name='status',
            field=models.CharField(default='agendado', max_length=10),
        ),
    ]
