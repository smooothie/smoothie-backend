# Generated by Django 3.0.2 on 2020-02-22 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_auto_20200111_1651'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='account_type',
            new_name='item_type',
        ),
    ]