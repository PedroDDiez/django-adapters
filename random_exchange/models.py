from django.db import models


class CurrencyLastExchange(models.Model):
    source_currency = models.CharField(max_length=3)
    exchanged_currency = models.CharField(max_length=3)
    rate = models.DecimalField(db_index=True, decimal_places=6, max_digits=18)
