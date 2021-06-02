from django.urls import path

from api.views import currency_rates, exchanged_currency_amount, twr

urlpatterns = [
    path(r'currency_rates', currency_rates),
    path(r'twr', twr),
    path(r'exchanged_currency_amount', exchanged_currency_amount),
]
