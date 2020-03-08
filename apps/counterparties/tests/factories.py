import factory

from apps.counterparties.models import Counterparty
from apps.users.tests.factories import UserFactory


class CounterpartyFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Faker('work')

    class Meta:
        model = Counterparty
