import factory

from apps.users.models import User


class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: f'user_{n}')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')

    class Meta:
        model = User
