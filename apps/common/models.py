from django.db import models
from django.db.utils import DEFAULT_DB_ALIAS

from polymorphic.models import PolymorphicModel


class PolyModel(PolymorphicModel):
    # denormalized field for easier type filters
    account_type = models.CharField(max_length=100, blank=True, default='', editable=False)

    class Meta:
        abstract = True

    def pre_save_polymorphic(self, using=DEFAULT_DB_ALIAS):
        if not self.polymorphic_ctype_id:
            super().pre_save_polymorphic(using)
            self.account_type = self.polymorphic_ctype.model
