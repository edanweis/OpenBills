# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

f = open('origin.txt')
soup = BeautifulSoup(f.read(), from_encoding='utf-8')

def readAccounts(account_types=['elec', 'gas']): # Allowed account types: "elec", or "gas"
	accounts = {}
	for account in account_types:
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

		accounts[account] = {"last_amount":last_amount, "last_date":last_date, "balance":balance, "due":due, "balance_discount":balance_discount}

	return accounts

print(readAccounts(['elec', 'gas']))