import factory

from apps.counterparties.models import Bank, Counterparty
from apps.users.tests.factories import UserFactory


class CounterpartyFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Faker('word')

    class Meta:
        model = Counterparty


class BankFactory(CounterpartyFactory):
    class Meta:
        model = Bank
