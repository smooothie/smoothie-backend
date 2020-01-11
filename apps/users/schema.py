from graphene import Field, relay
from graphene_django import DjangoObjectType

from apps.users.models import User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'accounts']
        interfaces = (relay.Node,)


class Query:
    user = Field(UserNode)

    def resolve_user(self, info):
        user = info.context.user
        if not user.is_authenticated:
            return None
        return user
