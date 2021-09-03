# Generated by Django 2.2.24 on 2021-08-24 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0049_auto_20210824_1426'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tests',
            name='indicators',
        ),
        migrations.RemoveField(
            model_name='tests',
            name='settings',
        ),
        migrations.AddField(
            model_name='tests',
            name='profit',
            field=models.FloatField(default=0, verbose_name='Прибыль'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tests',
            name='text',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Данные'),
        ),
        migrations.AddField(
            model_name='tests',
            name='win_rate',
            field=models.IntegerField(default=0, verbose_name='WIN %'),
            preserve_default=False,
        ),
    ]