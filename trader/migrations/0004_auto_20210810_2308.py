# Generated by Django 2.2.24 on 2021-08-10 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0003_variables_exсhange'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Variables',
            new_name='Strategy',
        ),
        migrations.RenameField(
            model_name='strategy',
            old_name='exсhange',
            new_name='exchange',
        ),
    ]