from datetime import datetime

from django.conf import settings
from rest_framework.exceptions import ValidationError, NotFound

from exchange_rate.models import Currency


def empty_params_validator(*args):
    for arg in args:
        if arg is None:
            raise ValidationError('One or more mandatory params are missing.')


def currency_available_validator(currency):
    if currency not in settings.AVAILABLE_CURRENCIES:
        raise NotFound('Currency "%s" not found. ' % currency)
    return Currency.objects.filter(symbol=currency).first()


def date_validator(str_date):
    try:
        return datetime.strptime(str_date, '%Y-%m-%d').date()
    except Exception as e:
        raise ValidationError('Invalid date format. Should be YYYY-MM-DD: ' + str(e))


def float_validator(amount):
    try:
        return float(amount)
    except Exception as e:
        raise ValidationError('"amount" should be a float: ' + str(e))
