from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from djmoney.models.fields import MoneyField

from apps.accounts.models import Account
from apps.common.models import PolyModel
from apps.common.validators import MinMoneyValidator
from apps.counterparties.models import Counterparty


class TransactionCategory(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = _('transaction categories')

    def __str__(self):
        return self.name


class Transaction(PolyModel):
    date = models.DateTimeField(default=timezone.now)
    amount = MoneyField(max_digits=14, decimal_places=2, validators=[MinMoneyValidator(0.01)])
    account_from = models.ForeignKey(Account, on_delete=models.PROTECT,
                                     related_name='transactions_from')
    account_to = models.ForeignKey(Account, on_delete=models.PROTECT,
                                   related_name='transactions_to')
    description = models.TextField(blank=True, default='')
    category = models.ForeignKey(TransactionCategory, on_delete=models.PROTECT,
                                 related_name='transactions')
    is_completed = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.date}, {self.amount}'


class Purchase(Transaction):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.SET_NULL, null=True,
                                     related_name='sales')


class Income(Transaction):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.SET_NULL, null=True,
                                     related_name='spendings')


class Transfer(Transaction):
    pass
