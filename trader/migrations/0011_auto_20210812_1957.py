# Generated by Django 2.2.24 on 2021-08-12 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0010_auto_20210812_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategy',
            name='limit_orders_buy',
            field=models.BooleanField(default=False, verbose_name='Закупка по лимитам'),
        ),
        migrations.AlterField(
            model_name='strategy',
            name='pair',
            field=models.CharField(max_length=25, verbose_name='Пара'),
        ),
    ]
