from django.core.exceptions import ValidationError
from django.db import models
from django.db.utils import DEFAULT_DB_ALIAS

from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from polymorphic.models import PolymorphicModel

from apps.users.models import User


class Account(PolymorphicModel):
    # denormalized field for easier type filters
    account_type = models.CharField(max_length=100, blank=True, default='', editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=128)
    balance = MoneyField(max_digits=14, decimal_places=2, default=0, default_currency='UAH')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique_user_name'
            ),
            models.UniqueConstraint(
                fields=['user', 'account_type'],
                name='unique_user_account_type',
                condition=models.Q(account_type__in=['spendingbalance', 'incomebalance'])
            ),
            models.CheckConstraint(
                check=models.Q(balance__gte=0) | ~models.Q(account_type='cashaccount'),
                name='positive_balance_debit'
            )
        ]

    def pre_save_polymorphic(self, using=DEFAULT_DB_ALIAS):
        if not self.polymorphic_ctype_id:
            super().pre_save_polymorphic(using)
            self.account_type = self.polymorphic_ctype.model

    def __str__(self):
        return f'{self.name}'


class SpendingBalance(Account):
    pass


class IncomeBalance(Account):
    pass


class DebitAccount(Account):
    class Meta:
        abstract = True

    def clean(self):
        balance_validator = MinMoneyValidator(0)
        try:
            balance_validator(self.balance)
        except ValidationError as e:
            raise ValidationError({'balance': e})


class CashAccount(DebitAccount):
    pass
