# Generated by Django 2.2.24 on 2021-08-17 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0039_auto_20210817_1740'),
    ]

    operations = [
        migrations.RenameField(
            model_name='position',
            old_name='base',
            new_name='amount_base',
        ),
    ]
