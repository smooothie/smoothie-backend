from django.core.validators import MinValueValidator


class MinMoneyValidator(MinValueValidator):
    def clean(self, x):
        return x.amount
