# Generated by Django 2.2.24 on 2021-09-19 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0055_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='options',
            name='expiration',
            field=models.IntegerField(default=None, verbose_name='Экспирация'),
            preserve_default=False,
        ),
    ]