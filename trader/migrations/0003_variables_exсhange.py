# Generated by Django 2.2.24 on 2021-08-10 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0002_variables_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='variables',
            name='exсhange',
            field=models.CharField(default='Kucoin', max_length=250, verbose_name='Биржа>'),
            preserve_default=False,
        ),
    ]
