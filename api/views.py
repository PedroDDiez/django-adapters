from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .validators import currency_available_validator, empty_params_validator, date_validator, float_validator
from exchange_rate.utils import get_currency_rates, get_exchanged_currency_amount, get_time_weighted_rate_return


@api_view(['GET'])
def currency_rates(request):
    """ Currency rates for a specific time period
    Parameters: source_currency: source currency symbol/ date_from / date_to
    Response: a time series list of rate values for each available Currency
    """
    # Get params
    currency_symbol = request.GET.get('source_currency')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    # Validate params
    empty_params_validator(currency_symbol, date_from, date_to)
    source_currency = currency_available_validator(currency_symbol)
    start_date = date_validator(date_from)
    end_date = date_validator(date_to)

    # Get data
    data = get_currency_rates(source_currency, start_date, end_date)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def exchanged_currency_amount(request):
    """ Calculates (latest) amount in a currency exchanged into a different currency.
    Parameters: source_currency, amount, exchanged_currency.
    Response: an object containing the rate value between source and exchanges currencies, along with the currencies.
    """
    # Get params
    source_currency_symbol = request.GET.get('source_currency')
    exchanged_currency_symbol = request.GET.get('exchanged_currency')
    amount = request.GET.get('amount')

    # Validate params
    empty_params_validator(source_currency_symbol, exchanged_currency_symbol, amount)
    source_currency = currency_available_validator(source_currency_symbol)
    exchanged_currency = currency_available_validator(exchanged_currency_symbol)
    amount = float_validator(amount)

    # Get data
    data = get_exchanged_currency_amount(source_currency, exchanged_currency, amount)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def twr(request):
    """ time-weighted rate of return for any given amount invested from a currency into another one from given date
    until today:
    Parameters: source_currency, amount, exchanged_currency, start_date
    Response: an object containing the rate value between source and exchanges currencies along with the currencies and
              start_date
    """
    source_currency_symbol = request.GET.get('source_currency')
    exchanged_currency_symbol = request.GET.get('exchanged_currency')
    amount = request.GET.get('amount')
    date_from = request.GET.get('date_from')

    # Validate params
    empty_params_validator(source_currency_symbol, exchanged_currency_symbol, amount, date_from)
    source_currency = currency_available_validator(source_currency_symbol)
    exchanged_currency = currency_available_validator(exchanged_currency_symbol)
    start_date = date_validator(date_from)
    amount = float_validator(amount)

    # Get data
    data = get_time_weighted_rate_return(source_currency, exchanged_currency, start_date, amount)
    return Response(data, status=status.HTTP_200_OK)
