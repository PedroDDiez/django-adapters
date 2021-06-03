# Generated by Django 3.2.3 on 2021-05-30 23:05
from django.conf import settings
from django.db import migrations

from exchange_rate.models import Currency, Provider


def load_currencies(apps, schema_editor):
    for currency in settings.CURRENCIES:
        Currency.objects.create(**currency)


def load_providers(apps, schema_editor):
    Provider.objects.create(**{'name': 'Fixer', 'priority': 1, 'adapter': 'exchange_rate.adapters.FixerAdapter'})
    Provider.objects.create(**{'name': 'Mock', 'priority': 2, 'adapter': 'exchange_rate.adapters.MockAdapter'})


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_rate', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_currencies, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(load_providers, reverse_code=migrations.RunPython.noop),
    ]
