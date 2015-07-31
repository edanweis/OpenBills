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
import requests


class Parse(object):

	def __init__(self, provider, service, accounts=[]):
		self.provider = provider
		self.accounts = accounts
		self.service = service



	def originEnergy(self):
		try:
			browser.visit("https://online.originenergy.com.au")
			browser.fill_form({'j_user': username, 'j_password': password})
			browser.find_by_name('uidPasswordLogon').first.click()
			if browser.is_text_present('Welcome'):
				with browser.get_iframe("ivuFrm_page0ivu1") as iframe1:  # isolatedWorkArea  ivuFrm_page0ivu4 ivuFrm_page0ivu4 sapPopupMainId_X0	obnNavIFrame externalLogOffIframe
					with iframe1.get_iframe("isolatedWorkArea") as iframe2:
						bill = iframe2.html
						# with open("origin.txt", 'w') as f:
						# 	f.write(bill)
				broswer.find_by_name('logout_submit').first.click()
			else:
				print("login was unsuccessful, try a different password")
			browser.quit()
		except: 
			browser.quit()

		
		soup = BeautifulSoup(bill, encoding="utf-8")
		self.result = {}
		
		for account in self.accounts:
			# find account section
			tr = soup.find('span', class_=account).find_previous('tr')
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

			result[account] = {"last_amount":last_amount, "last_date":last_date, "balance":balance, "due":due, "balance_discount":balance_discount}

		return self.result

	def fakeS(self):
		fake_result = "blah"
		return fake_result
	
	def details():
		return self.