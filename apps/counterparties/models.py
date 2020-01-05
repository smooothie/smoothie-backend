from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import PolyModel


class Counterparty(PolyModel):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = _('counterparties')

    def __str__(self):
        return f'{self.name}'


class Person(Counterparty):
    class Meta:
        verbose_name_plural = _('people')


class Organization(Counterparty):
    class Meta:
        abstract = True


class Bank(Organization):
    pass


class Shop(Organization):
    pass
