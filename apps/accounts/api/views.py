from rest_framework import viewsets
from rest_framework.decorators import action

from apps.accounts.filters import AccountFilter
from apps.accounts.models import Account
from .serializers import AccountSerializer, SimpleAccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.visible()
    serializer_class = AccountSerializer
    filterset_class = AccountFilter

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'options':
            return SimpleAccountSerializer
        return super().get_serializer_class()

    @action(['get'], detail=False)
    def options(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
