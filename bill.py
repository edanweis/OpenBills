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
import requests, configparser
from fuzzywuzzy import process

class Bill(object): 

    def __init__(self, provider, services=[], accounts=[]):
        self.provider = provider
        self.accounts = accounts
        self.services = services

        self.credentials = self.get_credentials()
        
        # Initialise browser
        # self.browser = Browser("phantomjs")
        
        # Initialise broweser (for debugging)
        self.browser = Browser()

        self.getBill() 
        


    def get_credentials(self):
        # Collect credentials
        config = configparser.ConfigParser()
        config.read('credentials.cfg')      
        provider = process.extractOne(self.provider, config.sections())[0]
        credentials = (config[provider]['username'], config[provider]['password'])
        return credentials

    def getBill(self):
        # Or create a dictionary from known list of provider parsing methods??
        # How does this actually work? Why does it execute the function? It's just a dict.
        provider_lookup = {"Origin Energy": self.originEnergy(), "example": self.example()}
        self.providers = list(provider_lookup.keys())

        eval(provider_lookup.get(process.extractOne(self.provider, self.providers)[0], "notFound")) # Ugly?

        return 

    def notFound(self):
        return "provider not found"

    def credentials(self):
        credentials = self.credentials
        return credentials

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
    


###################################################
# Everyone add your parsers here ###########


    def example(self):
        try:
            self.browser.visit("https://www.yourenergycompany.com")
            self.browser.fill_form({'user': self.credentials[0], 'pass': self.credentials[1]})
            self.browser.find_by_name('use__an_inspector').first.click()
        except:
            print('we want real exception handling.')
        pass

    def originEnergy(self):
        try:
            self.browser.visit("https://online.originenergy.com.au")
            self.browser.fill_form({'j_user': self.credentials[0], 'j_password': self.credentials[1]})
            self.browser.find_by_name('uidPasswordLogon').first.click()
            if self.browser.is_text_present('Welcome'):
                with self.browser.get_iframe("ivuFrm_page0ivu1") as iframe1:  # isolatedWorkArea  ivuFrm_page0ivu4 ivuFrm_page0ivu4 sapPopupMainId_X0   obnNavIFrame externalLogOffIframe
                    with iframe1.get_iframe("isolatedWorkArea") as iframe2:
                        bill_html = iframe2.html
                        # with open("origin.txt", 'w') as f:
                        #   f.write(bill)
                broswer.find_by_name('logout_submit').first.click()
            else:
                print("login was unsuccessful, try a different password")
            self.browser.quit()
        except: 
            self.browser.quit()

        soup = BeautifulSoup(bill_html)
        self.result = {}

        # use some variant of the "service" string to identify a link, section or page in the providers website. Here I point to the class "elec", hence service[:4].

        for service in self.services:
            # find account section shorten the service to the first or less words 
            tr = soup.find('span', class_=service[:4]).find_previous('tr')
            acc = tr.find('dd').get_text()

            # get last payment details
            last_amountdate = tr.find('dt', text='Last payment').find_previous('dl').find('span', class_='amount').get_text()
            last_amount = last_amountdate.strip().split('\n')[0].replace('$','')

            last_date = last_amountdate.strip().split('\n')[-1].strip()

            # In case no previous payments were made, last_date and last_amount contains "dummy" spans with false info, so replace those with an empty string.
            if '$' in last_date:
                last_date = None
                last_amount = None

            #get current payment details
            balance = tr.find('b', text='Account balance').find_previous('td', class_='major').find('span', class_='neg').get_text().strip().replace('$', '')
            due = tr.next_sibling.next_sibling.find('td', class_='major').find('b', text='Due date').find_previous('span').get_text().replace('Due date', '').strip()
            balance_discount = tr.next_sibling.next_sibling.find('td', class_='major').find('div', class_='money').get_text().strip().replace('$', '')

            self.result[service] = {"last_amount":last_amount, "last_date":last_date, "balance":balance, "due":due, "balance_discount":balance_discount}

        return self.result

    