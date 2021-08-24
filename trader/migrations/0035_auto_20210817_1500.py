# Generated by Django 2.2.24 on 2021-08-17 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0034_auto_20210817_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='amount_eth',
        ),
        migrations.AddField(
            model_name='position',
            name='base',
            field=models.FloatField(blank=True, null=True, verbose_name='base'),
        ),
    ]