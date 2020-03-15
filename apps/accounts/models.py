from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from polymorphic.managers import PolymorphicQuerySet

from apps.common.models import PolyModel
from apps.counterparties.models import Bank, Counterparty
from apps.users.models import User


class AccountQuerySet(PolymorphicQuerySet):
    def visible(self):
        return self.exclude(item_type__in=['incomebalance', 'spendingbalance'])


class Account(PolyModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=128)
    balance = MoneyField(max_digits=14, decimal_places=2, default=0, default_currency='UAH')
    credit_limit = models.DecimalField(max_digits=14, decimal_places=2, default=0,
                                       validators=[MinValueValidator(0)])

    objects = AccountQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='account_unique_user_name'
            ),
            models.UniqueConstraint(
                fields=['user', 'item_type', 'balance_currency'],
                name='unique_user_item_type',
                condition=models.Q(item_type__in=['spendingbalance', 'incomebalance'])
            ),
            models.CheckConstraint(
                check=(models.Q(balance__gte=0 - models.F('credit_limit'))),
                name='check_balance'
            ),
            models.CheckConstraint(
                check=(models.Q(credit_limit=0) |
                       ~models.Q(item_type__in=['cashaccount', 'deposit'])),
                name='positive_balance_debit'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.user.username}'

    def clean(self):
        balance_validator = MinMoneyValidator(0 - self.credit_limit)
        try:
            balance_validator(self.balance)
        except ValidationError as e:
            raise ValidationError({'balance': e})


class UnlimitedCreditAccount(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.credit_limit = 999999999
        return super().save(*args, **kwargs)

    def clean(self):
        self.credit_limit = 999999999
        super().clean()


class SpendingBalance(UnlimitedCreditAccount, Account):
    pass


class IncomeBalance(UnlimitedCreditAccount, Account):
    pass


class DebitAccount(Account):
    class Meta:
        abstract = True

    def clean(self):
        if self.credit_limit > 0:
            raise ValidationError({
                'credit_limit': 'Кредитний ліміт дебетового рахунку не може бути додатним',
            })
        super().clean()


class CashAccount(DebitAccount):
    pass


class CounterpartyAccount(UnlimitedCreditAccount, Account):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.PROTECT,
                                     related_name='accounts')


class BankAccountBase(Account):
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT)
    api_account_id = models.CharField(null=True, blank=True, unique=True, max_length=50)

    class Meta:
        abstract = True


class BankAccount(BankAccountBase):
    pass


class TermAgreementMixin(models.Model):
    class Meta:
        abstract = True

    PRINCIPAL_PAYMENT_METHOD_CHOICES = [
        ('equal_payment', 'Рівними частинами'),
        ('equal_instalment', 'Основна сума рівними частинами'),
        ('one_time', 'В кінці строку'),
        ('custom_scheme', 'Кастомізована схема'),
    ]

    INTEREST_PAYMENT_METHOD = [
        ('monthly_payment', 'Щомісячна виплата'),
        ('monthly_capital', 'Щомісячне додавання до основної суми'),
        ('one_time', 'В кінці строку'),
    ]

    interest_rate = models.FloatField(validators=[MinValueValidator(0.0)])
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    principal_payment_method = models.CharField(choices=PRINCIPAL_PAYMENT_METHOD_CHOICES,
                                                default='one_time',
                                                max_length=40)
    interest_payment_method = models.CharField(choices=INTEREST_PAYMENT_METHOD,
                                               default='monthly_payment',
                                               max_length=40)


class Deposit(TermAgreementMixin, DebitAccount, BankAccountBase):
    pass


class Loan(TermAgreementMixin, BankAccountBase):
    pass
