# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from splinter import Browser, cookie_manager
import requests, configparser


def originEnergy():
	username = config['originEnergy']['username']
	password = config['originEnergy']['password']
	try:
		browser.visit("https://online.originenergy.com.au")
		browser.fill_form({'j_user': username, 'j_password': password})
		browser.find_by_name('uidPasswordLogon').first.click()
		if browser.is_text_present('Welcome'):
			with browser.get_iframe("ivuFrm_page0ivu1") as iframe1:  # isolatedWorkArea  ivuFrm_page0ivu4 ivuFrm_page0ivu4 sapPopupMainId_X0	obnNavIFrame externalLogOffIframe
				with iframe1.get_iframe("isolatedWorkArea") as iframe2:
					bill = iframe2.html
					with open("origin.txt", 'w') as f:
						f.write(bill)
			broswer.find_by_name('logout_submit').first.click()
		else:
			print("login was unsuccessful, try a different password")
		browser.quit()
	except: 
		browser.quit()
	return bill

def billme():
	global config, browser
	browser = Browser()
	config = configparser.ConfigParser()
	config.read('credentials.cfg')
	
	originEnergy()
	
	return

if __name__ == '__main__':
	billme()