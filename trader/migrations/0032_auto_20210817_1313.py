# Generated by Django 2.2.24 on 2021-08-17 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0031_auto_20210817_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='close',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='history',
            name='high',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='history',
            name='low',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='history',
            name='open',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='history',
            name='volume',
            field=models.FloatField(),
        ),
    ]