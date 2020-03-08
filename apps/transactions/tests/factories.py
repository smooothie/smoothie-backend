import factory

from apps.accounts.tests.factories import CashAccountFactory
from apps.counterparties.tests.factories import CounterpartyFactory
from apps.transactions.models import Income, Purchase, TransactionCategory, Transfer


class TransactionCategoryFactory(factory.DjangoModelFactory):
    name = factory.Faker('word')

    class Meta:
        model = TransactionCategory


class TransactionFactory(factory.DjangoModelFactory):
    account_from = factory.SubFactory(CashAccountFactory)
    account_to = factory.SubFactory(CashAccountFactory)
    category = factory.SubFactory(TransactionCategoryFactory)

    class Meta:
        abstract = True


class TransferFactory(TransactionFactory):
    class Meta:
        model = Transfer


class IncomeFactory(TransactionFactory):
    counterparty = factory.SubFactory(CounterpartyFactory)

    class Meta:
        model = Income


class PurchaseFactory(TransactionFactory):
    counterparty = factory.SubFactory(CounterpartyFactory)

    class Meta:
        model = Purchase
