# Generated by Django 3.0.2 on 2020-01-11 14:51

import apps.common.validators
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_remove_transactioncategory_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, max_digits=14, validators=[apps.common.validators.MinMoneyValidator(0.01)]),
        ),
    ]
