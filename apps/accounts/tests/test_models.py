from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from parameterized import parameterized

from apps.accounts.models import IncomeBalance, SpendingBalance
from apps.users.tests.factories import UserFactory
from .factories import CashAccountFactory, IncomeBalanceFactory, SpendingBalanceFactory


class AccountTestCase(TestCase):
    @parameterized.expand([
        ('cashaccount', CashAccountFactory),
        ('incomebalance', IncomeBalanceFactory),
        ('spendingbalance', SpendingBalanceFactory),
    ])
    def test_sets_account_type(self, account_type, model_factory):
        account = model_factory()
        self.assertEqual(account.account_type, account_type)

    @parameterized.expand([
        ('cashaccount', CashAccountFactory),
        ('incomebalance', IncomeBalanceFactory),
        ('spendingbalance', SpendingBalanceFactory),
    ])
    def test_checks_unique_account_name_per_user(self, account_type, model_factory):
        account = model_factory()
        new_account = model_factory.build(user=account.user, name=account.name)
        with self.assertRaises(ValidationError):
            new_account.full_clean()
        with self.assertRaises(IntegrityError):
            new_account.save()

    def test_creates_account_on_user_creation(self):
        user = UserFactory()
        self.assertEqual(user.accounts.count(), 2)
        self.assertCountEqual(user.accounts.values_list('account_type', flat=True),
                              ['incomebalance', 'spendingbalance'])

    @parameterized.expand([
        ('incomebalance', IncomeBalance),
        ('spendingbalance', SpendingBalance),
    ])
    def test_checks_unique_account_type_per_user(self, account_type, model):
        user = UserFactory()

        # cash accounts for the same user are created normally
        CashAccountFactory(user=user)
        CashAccountFactory(user=user)

        with self.assertRaises(IntegrityError):
            model.objects.create(user=user, name=f'{account_type} 1')

    def test_checks_negative_balance(self):
        spending_account = SpendingBalanceFactory()
        spending_account.balance = -300
        self.assertIsNone(spending_account.full_clean())
        spending_account.save()
        self.assertEqual(spending_account.balance.amount, -300)

        cash_account = CashAccountFactory()
        cash_account.balance = -300

        with self.assertRaises(ValidationError):
            cash_account.full_clean()

        with self.assertRaises(IntegrityError):
            cash_account.save()
