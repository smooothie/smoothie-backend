# Generated by Django 3.0.2 on 2020-02-22 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('counterparties', '0003_auto_20200126_1607'),
    ]

    operations = [
        migrations.RenameField(
            model_name='counterparty',
            old_name='account_type',
            new_name='item_type',
        ),
    ]
