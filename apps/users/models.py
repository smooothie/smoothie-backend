from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import CIEmailField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = CIEmailField(
        verbose_name=_('Email'),
        max_length=254,
        unique=True,
        error_messages={
            'unique': _('That email address is already taken.')
        }
    )
