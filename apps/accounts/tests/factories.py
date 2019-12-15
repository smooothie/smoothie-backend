import factory

from apps.accounts.models import CashAccount, IncomeBalance, SpendingBalance
from apps.users.tests.factories import UserFactory


class AccountFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'Account {n}')

    class Meta:
        abstract = True


class SpendingBalanceFactory(AccountFactory):
    class Meta:
        model = SpendingBalance
        django_get_or_create = ('user',)


class IncomeBalanceFactory(AccountFactory):
    class Meta:
        model = IncomeBalance
        django_get_or_create = ('user',)


class CashAccountFactory(AccountFactory):
    class Meta:
        model = CashAccount
