# Generated by Django 2.2.24 on 2021-08-19 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0043_history_timeframe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='timeframe',
            field=models.CharField(choices=[('1m', 'Минута'), ('1h', 'Час')], max_length=25, verbose_name='Таймфрейм'),
        ),
    ]