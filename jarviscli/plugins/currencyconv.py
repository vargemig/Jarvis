import os
import csv

from decimal import Decimal

from six.moves import input

from plugin import plugin, require
from utilities.GeneralUtilities import get_float

from forex_python.bitcoin import BtcConverter
from forex_python.converter import CurrencyRates


FILE_PATH = os.path.abspath(os.path.dirname(__file__))


@require(network=True)
@plugin
class Currencyconv():
    """
    Convert an amount of money from a currency to another.
    -- Type currencyconv, press enter and follow the instructions!
    """
    def __call__(self, jarvis, s):
        currencies = self.find_currencies()

        amount = get_float('Enter an amount: ')
        from_currency = self.get_currency('Enter from which currency: ', currencies)
        to_currency = self.get_currency('Enter to which currency: ', currencies)

        self.currencyconv(jarvis, amount, from_currency, to_currency)

    def currencyconv(self, jarvis, amount, fr, to):
        """
        currencyconv converts the given amount to another currency
        using fore-python
        """

        b = BtcConverter(force_decimal=True)
        c = CurrencyRates(force_decimal=True)

        if (to == "BTC"):
            result = b.convert_to_btc(Decimal(amount), fr)
        elif (fr == "BTC"):
            result = b.convert_btc_to_cur(Decimal(amount), to)
        else:
            result = c.convert(fr, to, Decimal(amount))

        jarvis.say(str(result))

    def find_currencies(self):
        """
        find_currency creates a dict with the inputs that forex-python accepts
        """

        with open(os.path.join(FILE_PATH, "../data/currencies.csv"), mode='r') as infile:
            reader = csv.reader(infile)
            mydict = {r.upper(): row[2] for row in reader for r in row[0:3]}
        return mydict

    def get_currency(self, prompt, currencies):
        """
        get_currency checks if the input the user gave is valid based
        on the dictionary of find_currencies
        """

        while True:
            c = input(prompt).upper()
            if c in currencies:
                return currencies[c]
            elif c == "show help".upper():
                print(', '.join(set(currencies.values())))
                prompt = 'Please enter a valid country or currency: '
                continue
            elif c == "try again".upper():
                prompt = 'Please enter a valid country or currency: '
                continue
            else:
                prompt = 'Type -show help- to see valid currencies '\
                         'or -try again- to continue: '
