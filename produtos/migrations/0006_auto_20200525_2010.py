# Generated by Django 3.0.6 on 2020-05-25 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0005_auto_20200506_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtos',
            name='nome',
            field=models.CharField(max_length=80),
        ),
    ]