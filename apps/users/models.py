from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import CIEmailField
from django.utils.translation import gettext_lazy as _

from djmoney.money import Money


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = CIEmailField(
        verbose_name=_('Email'),
        max_length=254,
        unique=True,
        error_messages={
            'unique': _('That email address is already taken.')
        }
    )

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        return super().save(*args, **kwargs)

    def get_income_balance(self, currency):
        from apps.accounts.models import IncomeBalance
        return IncomeBalance.objects.get_or_create(
            user=self,
            balance_currency=currency,
            defaults={'name': f'Рахунок доходів {currency}', 'balance': Money(0, currency)}
        )[0]

    def get_spending_balance(self, currency):
        from apps.accounts.models import SpendingBalance
        return SpendingBalance.objects.get_or_create(
            user=self,
            balance_currency=currency,
            defaults={'name': f'Рахунок витрат {currency}', 'balance': Money(0, currency)}
        )[0]
