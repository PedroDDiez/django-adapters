from django.contrib import admin

# Register your models here.
from .models import Provider, CurrencyExchangeRate, Currency


class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    fields = ['source_currency', 'exchanged_currency', 'valuation_date', 'rate_value']
    list_display = ['source_currency', 'exchanged_currency', 'valuation_date', 'rate_value']
    ordering = ('source_currency', 'exchanged_currency', '-valuation_date')


class CurrencyAdmin(admin.ModelAdmin):
    fields = ['code', 'name', 'symbol']


class ProviderAdmin(admin.ModelAdmin):
    fields = ['name', 'priority', 'adapter']
    list_display = ['name', 'priority', 'adapter']
    ordering = ('priority',)


admin.site.register(CurrencyExchangeRate, CurrencyExchangeRateAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Provider, ProviderAdmin)
