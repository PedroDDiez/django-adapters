from rest_framework import status
from rest_framework.test import APITestCase

from exchange_rate.models import Provider


class CurrencyRatesTestCase(APITestCase):
    def test_currency_rates_fixer(self):
        """
        Ensure we can get currency rates from fixer
        """
        Provider.objects.filter(name='Fixer').update(priority=1)
        Provider.objects.filter(name='Mock').update(priority=2)

        url = 'http://127.0.0.1:8000/api/currency_rates?source_currency=EUR&date_from=2021-02-08&date_to=2021-02-14'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 7)

    def test_currency_rates_mock(self):
        """
        Ensure we can get currency rates from mock
        """
        Provider.objects.filter(name='Mock').update(priority=1)
        Provider.objects.filter(name='Fixer').update(priority=2)
        url = 'http://127.0.0.1:8000/api/currency_rates?source_currency=EUR&date_from=2021-02-15&date_to=2021-02-21'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 7)

    def test_currency_rates_db_and_provider(self):
        """
        Ensure we can get currency rates from both db and provider
        """
        Provider.objects.filter(name='Fixer').update(priority=1)
        Provider.objects.filter(name='Mock').update(priority=2)
        url = 'http://127.0.0.1:8000/api/currency_rates?source_currency=EUR&date_from=2021-02-01&date_to=2021-02-28'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 28)

    def test_currency_rates_param_errors(self):
        """
        Ensure we get error status on param errors
        """
        # Invalid date
        url = 'http://127.0.0.1:8000/api/currency_rates?source_currency=EUR&date_from=2021-05-15&date_to=201-05-22'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Invalid currency
        url = 'http://127.0.0.1:8000/api/currency_rates?source_currency=EURO&date_from=2021-05-15&date_to=2021-05-22'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Missing param
        url = 'http://127.0.0.1:8000/api/currency_rates?source_currency=EUR&date_from=2021-05-15'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ExchangedCurrencyAmountTestCase(APITestCase):
    def test_exchanged_currency_amount(self):
        """
        Ensure we can get amount exchanged
        """
        url = 'http://127.0.0.1:8000/api/exchanged_currency_amount?source_currency=EUR&exchanged_currency=GBP&amount=1.3'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'rate')
        self.assertContains(response, 'exchanged_amount')

    def test_exchanged_currency_amount_param_errors(self):
        """
        Ensure we get error status on param errors
        """
        # Invalid amount
        url = 'http://127.0.0.1:8000/api/exchanged_currency_amount?source_currency=EUR&exchanged_currency=GBP&amount=a3'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Invalid currency
        url = 'http://127.0.0.1:8000/api/exchanged_currency_amount?source_currency=EU&exchanged_currency=GBP&amount=1.3'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Missing param
        url = 'http://127.0.0.1:8000/api/exchanged_currency_amount?source_currency=EUR&exchanged_currency=GBP'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TimeWeightedRateTestCase(APITestCase):
    def test_time_weight_rate(self):
        """
        Ensure we get error status on param errors
        """
        url = 'http://127.0.0.1:8000/api/twr?source_currency=EUR&exchanged_currency=GBP&amount=1.3&date_from=2020-05-15'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'twr')

    def test_time_weight_rate_param_errors(self):
        """
        Ensure we get error status on param errors
        """
        # Invalid date
        url = 'http://127.0.0.1:8000/api/twr?source_currency=EUR&exchanged_currency=GBP&amount=1.3&date_from=2020-15-15'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Invalid amount
        url = 'http://127.0.0.1:8000/api/twr?source_currency=EUR&exchanged_currency=GBP&amount=1,3&date_from=2020-05-15'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # invalid currency
        url = 'http://127.0.0.1:8000/api/twr?source_currency=EURO&exchanged_currency=GBP&amount=1,3&date_from=2020-05-15'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # invalid currency
        url = 'http://127.0.0.1:8000/api/twr?source_currency=EUR&exchanged_currency=BP&amount=12,3&date_from=2020-05-15'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # missing param
        url = 'http://127.0.0.1:8000/api/twr?source_currency=EURO&exchanged_currency=GBP&amount=1.3'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
