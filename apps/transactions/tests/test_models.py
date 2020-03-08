from django.db import IntegrityError
from django.test import TestCase

from djmoney.money import Money

from apps.accounts.tests.factories import CashAccountFactory
from .factories import TransferFactory


class TransactionModelTestCase(TestCase):
    def test_currency_integrity(self):
        cash1 = CashAccountFactory(balance=Money(50, 'UAH'))
        cash2 = CashAccountFactory(user=cash1.user, balance=(0, 'USD'))
        with self.assertRaises(IntegrityError):
            TransferFactory(account_from=cash1, account_to=cash2, amount=Money(30, 'UAH'))
