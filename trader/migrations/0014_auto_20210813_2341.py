# Generated by Django 2.2.24 on 2021-08-13 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0013_history'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='valume',
            new_name='volume',
        ),
    ]
