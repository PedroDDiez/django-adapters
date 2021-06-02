import random

from random_exchange.models import CurrencyLastExchange


class RandomClient(object):

    @classmethod
    def get_random_exchange(cls, source_currency, exchanged_currency):
        if source_currency == exchanged_currency:
            return 1.
        exchange = CurrencyLastExchange.objects.filter(source_currency=source_currency,
                                                       exchanged_currency=exchanged_currency).first()
        # If a exchange rate has been used for these currencies, generate a new similar one
        if exchange:
            rate = float(exchange.rate) * (1+random.randint(-100, 100)/10000.)
            exchange.rate = rate
            exchange.save()
        # If not exchange rate has been used, create a new one.
        else:
            rate = random.randint(0, 10000) / 100.
            CurrencyLastExchange.objects.create(source_currency=source_currency,
                                                exchanged_currency=exchanged_currency,
                                                rate=rate)
        return rate
