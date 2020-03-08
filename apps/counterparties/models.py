from django.contrib.postgres.fields import CICharField
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import PolyModel
from apps.users.models import User


class Counterparty(PolyModel):
    name = CICharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='counterparties')

    class Meta:
        verbose_name_plural = _('counterparties')
        constraints = [
            models.UniqueConstraint(fields=['user', 'name', 'item_type'],
                                    name='counterparty_unique_user_name'),
        ]

    def __str__(self):
        return f'{self.name}'


class Person(Counterparty):
    class Meta:
        verbose_name_plural = _('people')


class Organization(Counterparty):
    class Meta:
        abstract = True


class Bank(Organization):
    API_CHOICES = [
        ('MonobankAPI', 'Monobank API'),
    ]

    api_class = models.CharField(choices=API_CHOICES, null=True, blank=True, max_length=50)


class Shop(Organization):
    pass
