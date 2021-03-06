# Generated by Django 2.2.24 on 2021-09-19 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0054_auto_20210906_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('varian', models.CharField(max_length=250, verbose_name='Вариант')),
                ('buy_price', models.FloatField(verbose_name='Покупка')),
                ('strike', models.FloatField(blank=True, null=True, verbose_name='Страйк')),
                ('amount', models.FloatField(blank=True, null=True, verbose_name='Кол-во опциона')),
                ('opened', models.IntegerField(verbose_name='Открыт')),
                ('closed', models.IntegerField(null=True, verbose_name='Закрыт')),
                ('active', models.BooleanField(default='True', verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'Позиция',
                'verbose_name_plural': 'Позиции',
                'ordering': ['-opened'],
            },
        ),
    ]
