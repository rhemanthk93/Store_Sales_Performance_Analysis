# app/utilities/currency_conversion.py
import requests
from decimal import Decimal

class CurrencyConversion:
    def __init__(self):
        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self.exchange_rates = self.get_exchange_rates()

    def get_exchange_rates(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            rates = response.json().get('rates', {})
            return {currency: Decimal(str(rate)) for currency, rate in rates.items()}
        else:
            raise Exception("Failed to retrieve exchange rates")

    def convert_to_usd(self, amount, currency):
        if currency == 'RMB':
            currency = 'CNY'

        if currency == 'USD':
            return amount
        rate = self.exchange_rates.get(currency)
        if rate:
            return Decimal(str(amount)) / rate
        else:
            return None

    def convert_to_rmb(self, amount, currency):
        if currency == 'RMB':
            return amount
        usd_amount = self.convert_to_usd(amount, currency)
        rmb_rate = self.exchange_rates.get('CNY')  # 'CNY' is the standard code for Chinese Yuan Renminbi
        if usd_amount is not None and rmb_rate:
            return usd_amount * rmb_rate
        else:
            return None