from django.db import models
from django.db.transaction import atomic
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from djmoney.models.fields import MoneyField
from polymorphic.managers import PolymorphicQuerySet

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


class TransactionQuerySet(PolymorphicQuerySet):
    def for_user(self, user_id):
        return self.filter(
            models.Q(account_from__user_id=user_id) |
            models.Q(account_to__user_id=user_id)
        )

    def for_account(self, account_id):
        return self.filter(
            models.Q(account_from_id=account_id) |
            models.Q(account_to_id=account_id)
        )


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

    objects = TransactionQuerySet.as_manager()

    def __str__(self):
        return f'{self.date}, {self.amount}'

    def update_accounts_balances(self):
        self.account_from.balance -= self.amount
        self.account_to.balance += self.amount
        self.account_from.save(update_fields=['balance'])
        self.account_to.save(update_fields=['balance'])

    @atomic
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        res = super().save(*args, **kwargs)
        # TODO: handle updates as well
        if is_new and self.is_completed:
            self.update_accounts_balances()
        return res


class Purchase(Transaction):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.SET_NULL, null=True,
                                     related_name='sales')


class Income(Transaction):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.SET_NULL, null=True,
                                     related_name='spendings')


class Transfer(Transaction):
    pass
