from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import CIEmailField
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = CIEmailField(
        verbose_name=_('Email'),
        max_length=254,
        unique=True,
        error_messages={
            'unique': _('That email address is already taken.')
        }
    )

    @cached_property
    def income_balance(self):
        from apps.accounts.models import IncomeBalance
        return IncomeBalance.objects.get_or_create(
            user=self,
            defaults={'name': 'Income Balance'}
        )[0]

    @cached_property
    def spending_balance(self):
        from apps.accounts.models import SpendingBalance
        return SpendingBalance.objects.get_or_create(
            user=self,
            defaults={'name': 'Spending Balance'}
        )[0]
