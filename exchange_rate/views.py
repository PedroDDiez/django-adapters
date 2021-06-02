import numpy as np
import pandas as pd

from datetime import date

from django.shortcuts import render

from exchange_rate.models import Currency
from exchange_rate.utils import get_currency_rates


# Create your views here.
def dashboard(request, base_currency):
    source = Currency.objects.get(symbol__iexact=base_currency)
    rates = get_currency_rates(source, date(2021, 4, 20), date(2021, 5, 22))
    exchange_rates = pd.DataFrame([r['rates'] for r in rates])
    exchange_rates['timestamp'] = pd.DatetimeIndex([r['valuation_date'] for r in rates]).astype(np.int64) / 1000000

    return render(request, 'exchange_rate/dashboard.html', {'exchange_rates': exchange_rates.values.tolist(),
                                                            'source_currency': source,
                                                            'rates': exchange_rates.columns[:-1]})
