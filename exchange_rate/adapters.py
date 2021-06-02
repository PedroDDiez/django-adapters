"""
https://charlesleifer.com/blog/django-patterns-pluggable-backends/
"""
from datetime import datetime
from fixerio import Fixerio
from fixerio.exceptions import FixerioException

from django.conf import settings

from random_exchange.client import RandomClient
from exchange_rate.models import CurrencyExchangeRate, Currency


class BaseAdapter(object):
    def __init__(self):
        self.backend = self.get_backend()

    def get_backend(self):
        raise NotImplementedError

    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        """
        Since Python does not have interfaces, its common to raise
        NotImplementedErrors when specifying a base class that you wish to
        act as an interface.
        """
        raise NotImplementedError

    @classmethod
    def date_to_str(cls, str_date):
        return datetime.strftime(str_date, "%Y-%m-%d")

    @classmethod
    def parse_date(cls, d_date):
        return datetime.strptime(d_date, "%Y-%m-%d")

    @classmethod
    def convert_exchange_base(cls, exchange_values):
        """ Creates a list of exchange rates based on each currency in exchange_values['rates']

        :param exchange_values: exchange rates for a given base currency.
        :type exchange_values: dict
        :return: a list of based exchange rates
        :rtype: list of dict
        """
        bases = exchange_values['rates'].keys()
        rates = exchange_values['rates']
        exchange_rates = [{'base': base, 'date': exchange_values['date'],
                           'rates': {rate: rates[rate] / rates[base] for rate in rates}} for base in bases]

        return exchange_rates

    @classmethod
    def parse_currency(cls, symbol):
        return Currency.objects.get(symbol=symbol)

    @classmethod
    def parse_exchange_rates(cls, exchange_rates):
        """ Creates a list of CurrencyExchangeRate objects from a list of based exchange rates

        :param exchange_rates: list of based exchange rates.
        :type exchange_rates: list
        :return: a list of CurrencyExchangeRate objects
        :rtype: list of CurrencyExchangeRate
        """
        currency_exchange_rates = []
        for exchange in exchange_rates:
            source_currency_symbol = exchange['base']
            source_currency = cls.parse_currency(source_currency_symbol)
            for exchanged_currency_symbol in exchange['rates']:
                if source_currency_symbol != exchanged_currency_symbol:
                    exchanged_currency = cls.parse_currency(exchanged_currency_symbol)
                    cur_exchange_rate = CurrencyExchangeRate(source_currency=source_currency,
                                                             exchanged_currency=exchanged_currency,
                                                             valuation_date=cls.parse_date(exchange['date']),
                                                             rate_value=exchange['rates'][exchanged_currency_symbol])
                    currency_exchange_rates.append(cur_exchange_rate)
        return currency_exchange_rates

    def store_values(self, exchange_rates):
        """ Stores in database all rates from source based curency exchange rates

        :param exchange_rates: exchange rates for a given base currency.
        :type exchange_rates: list
        :return: a list of CurrencyExchangeRate objects
        :rtype: created CurrencyExchangeRate objects as a list
        """
        currency_exchange_rates = self.parse_exchange_rates(exchange_rates)
        return CurrencyExchangeRate.objects.bulk_create(currency_exchange_rates)


class FixerAdapter(BaseAdapter):

    def get_backend(self):
        return self.connect_to_fixer()

    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        try:
            exchange_values = self.backend.historical_rates(self.date_to_str(valuation_date))
        except FixerioException:
            return None
        if not exchange_values['success']:
            return None
        full_based_exchange_rates = self.convert_exchange_base(exchange_values)
        self.store_values(full_based_exchange_rates)

        for exchange_rates in full_based_exchange_rates:
            if exchange_rates['base'] == source_currency.symbol:
                return {'source_currency': source_currency.symbol, 'exchanged_currency': exchanged_currency.symbol,
                        'valuation_date': self.date_to_str(valuation_date),
                        'rate_value': exchange_rates['rates'][exchanged_currency.symbol]}
        return None

    @classmethod
    def connect_to_fixer(cls):
        return Fixerio(access_key=settings.FIXER_KEY, symbols=settings.AVAILABLE_CURRENCIES)


class MockAdapter(BaseAdapter):
    def get_backend(self):
        return self.connect_to_mock()

    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        rate = self.backend.get_random_exchange(source_currency, exchanged_currency)
        return {'source_currency': source_currency.symbol, 'exchanged_currency': exchanged_currency.symbol,
                'valuation_date': self.date_to_str(valuation_date), 'rate_value': rate}

    @classmethod
    def connect_to_mock(cls):
        return RandomClient()
