'''
    OpenBills
    Copyright (C) 2015  Edan Weis

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

'''

from bs4 import BeautifulSoup
from splinter import Browser, cookie_manager
import requests, configparser, parser
from fuzzywuzzy import process


class Bill(object): 

    def __init__(self, provider, services=[], accounts=[]):
        self.provider = provider
        self.accounts = accounts
        self.services = services

        self.credentials = get_credentials(provider)
        
        # Initialise browser
        # self.browser = Browser("phantomjs")
        
        # Initialise broweser (for debugging)
        self.browser = Browser()
        self.result = self.getBill()

    def getBill(self):
        function_names = [x for x in dir(parser) if x[0] is not "_"][1:]
        chosen_bill = process.extractOne(self.provider, function_names)
        # if fuzzy match is over 50% confidence:
        if chosen_bill[1] > 50:
            return getattr(parser, chosen_bill[0])(self.credentials, self.browser, self.services, self.accounts)
        else:
            self.browser.quit()
            return notFound(self.provider)

    def all(self):
        return self.result

    def info(self, service):
        try:
            return self.providorParse().get(service, "").get('info', "")
        except:
            return "no such service"

    def last_amount(self):
        return self.results['last_amount']

    def last_date(self):
        results = {}
        return results

    def balance(self):
        results = {}
        return results

    def due(self):
        results = {}
        return results

    def balance_discount(self):
        results = {}
        return results


def get_credentials(provider):
        # Collect credentials
        config = configparser.ConfigParser()
        config.read('credentials.cfg')      
        provider = process.extractOne(provider, config.sections())[0]
        credentials = (config[provider]['username'], config[provider]['password'])
        return credentials

def notFound(provider):
        return "Oops, we haven't opened %s bills yet! Try another?" % provider