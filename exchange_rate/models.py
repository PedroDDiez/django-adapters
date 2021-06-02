from django.db import models
from django.conf import settings
from importlib import import_module
# TODO:
#  Documentar:
#   - si se llena de golpe la base de datos, o sobre la marcha
#   - llamadas a fixer multifecha
#   - distintos providers ofrecen mismos datos
#   - prioridad: base de datos y providers en orden
#   - ya que tenemos varios provider, d que sirve pasarlo de parametro a get_exchange_rate_data
#   - API: no lleva autenticacion


class Provider(models.Model):
    name = models.CharField(max_length=50)
    priority = models.IntegerField()
    adapter = models.CharField(max_length=50, choices=settings.PROVIDER_ADAPTERS)

    def get_adapter(self):
        # grab the classname off of the backend string
        package, klass = self.adapter.rsplit('.', 1)

        # dynamically import the module, in this case app.backends.adapter_a
        module = import_module(package)

        # pull the class off the module and return
        return getattr(module, klass)

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.symbol


class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(Currency, related_name='exchanges', on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(db_index=True, decimal_places=6, max_digits=18)

    def __str__(self):
        return self.source_currency.symbol + '->' + self.exchanged_currency.symbol + ': ' + str(self.rate_value) + \
               ' (' + self.valuation_date.strftime('%Y-%m-%d') + ')'
