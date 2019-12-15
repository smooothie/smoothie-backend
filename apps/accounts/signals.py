from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import IncomeBalance, SpendingBalance
from apps.users.models import User


@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    if created:
        IncomeBalance.objects.create(user=instance, name='Income Balance')
        SpendingBalance.objects.create(user=instance, name='Spending Balance')
