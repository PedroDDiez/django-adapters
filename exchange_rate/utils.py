import pandas as pd

from datetime import date

from exchange_rate.models import CurrencyExchangeRate, Provider, Currency


def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider):
    """Get the exchange rate data from a given provider
    Parameters: source_currency / exchanged_currency / valuation_date / provider
    Response: dict with the exchange rate info
    """
    adapter = provider.get_adapter()
    return adapter().get_exchange_rate_data(source_currency, exchanged_currency, valuation_date)


def get_exchange_rate_data_db_providers(source_currency, exchanged_currency, valuation_date):
    """Get the exchange rate data looking for it first in the database, if not present there, get it from providers
    iterating over them in priority order
    Parameters: source_currency: source currency symbol/ valuation_date / provider
    Response: dict with the exchange rate info
    """
    if source_currency == exchanged_currency:
        return 1.
    rate = CurrencyExchangeRate.objects.filter(source_currency=source_currency,
                                               exchanged_currency=exchanged_currency,
                                               valuation_date=valuation_date).first()
    if rate:
        return float(rate.rate_value)
    # Rate is not in db, look for it in providers ordered by priority
    providers = Provider.objects.all().order_by('priority')
    for provider in providers:
        rate_data = get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider)
        if rate_data:
            return rate_data['rate_value']
    return None


def get_currency_rates(source_currency, start_date, end_date):
    """ Currency rates for a specific time period
    Parameters: source_currency / date_from / date_to
    Response: a time series list of rate values for each available Currency
    """
    currency_rates = []
    dates = pd.date_range(start_date, end_date)

    for valuation_date in dates:
        daily_currency_rate = {'source_currency': source_currency.symbol,
                               'valuation_date': valuation_date.strftime('%Y-%m-%d')}
        rates = {}
        for exchanged_currency in Currency.objects.all():
            rate = get_exchange_rate_data_db_providers(source_currency, exchanged_currency, valuation_date)
            rates[exchanged_currency.symbol] = rate
        daily_currency_rate['rates'] = rates
        currency_rates.append(daily_currency_rate)

    return currency_rates


def get_exchanged_currency_amount(source_currency, exchanged_currency, amount):
    """ Calculates (latest) amount in a currency exchanged into a different currency.
    Parameters: source_currency, exchanged_currency, amount.
    Response: an dict containing the exchanged amount along with the currencies and exchange rate.
    """
    rate = get_exchange_rate_data_db_providers(source_currency, exchanged_currency, date.today())
    return {'source_currency': source_currency.symbol, 'exchanged_currency': exchanged_currency.symbol,
            'rate': rate, 'exchanged_amount': amount * rate}


def get_time_weighted_rate_return(source_currency, exchanged_currency, start_date, amount):
    """ time-weighted rate of return for any given amount invested from a currency into another one from given date
    until today:
    Parameters: source_currency, exchanged_currency, start_date, amount
    Response: an dict containing the rate value between source and exchanges currencies along with the currencies and
              start_date
    """

    # TWR = [(1+HP1​)x(1+HP2​)x···x(1+HPn​)]−1 = Time-weighted return
    # n = Number of sub-periods
    # HP = (end_value - initial_value + cash_flow) / (initial_value + cash_flow)
    cash_flow = 0
    initial_rate = get_exchange_rate_data_db_providers(source_currency, exchanged_currency, start_date)
    end_rate = get_exchange_rate_data_db_providers(source_currency, exchanged_currency, date.today())
    if not initial_rate or not end_rate:
        return None
    initial_value = amount * initial_rate
    end_value = amount * end_rate
    twr = (end_value - initial_value + cash_flow) / (initial_value + cash_flow)
    data = {'source_currency': source_currency.symbol, 'exchanged_currency': exchanged_currency.symbol,
            'date_from': start_date.strftime('%Y-%m-%d'), 'amount': amount, 'twr': twr}

    return data
