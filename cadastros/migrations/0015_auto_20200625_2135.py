# Generated by Django 3.0.6 on 2020-06-26 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0014_problemas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemas',
            name='Email',
            field=models.CharField(max_length=100, verbose_name='Email Que você usa no Site'),
        ),
    ]
