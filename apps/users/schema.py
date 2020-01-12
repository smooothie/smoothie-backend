from graphene import Field, relay
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from apps.users.models import User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'accounts']
        interfaces = (relay.Node,)


class Query:
    user = Field(UserNode)

    @login_required
    def resolve_user(self, info):
        return info.context.user
