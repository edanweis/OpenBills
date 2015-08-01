from bs4 import BeautifulSoup


# Add your BeautifulSoup and splinter code here. Give your function the same name as the energy provider. For example:

def myEnergyCompany(credentials, browser, services=["electricity", "gas"], accounts=[]): 
    try:
        browser.visit("https://www.yourenergycompany.com")
        browser.fill_form({'user': credentials[0], 'pass': credentials[1]})
        browser.find_by_name('use__an_inspector').first.click()
        # get to the page with the desired billing information you would like to parse. 
        bill_html = browser.html
    except:
        print('we want real exception handling.')
        browser.quit()
    
    #now parse the html result:
    soup = BeautifulSoup(bill_html)
    result={}
    # use some variant of the "service" string to identify a link, section or page in the providers website.
    for service in services: 
        # do some parsing to get to the data you want, and store the results (ie: replace "None", with your extracted data )
        result['last_amount'] = None
        result['last_date'] = None
        result['balance'] = None
        result['due'] = None
        result['balance_discount'] = None

    return result






#################

def originEnergy(credentials, browser, services=["electricity", "gas"], accounts=[]):
    try:
        browser.visit("https://online.originenergy.com.au")
        browser.fill_form({'j_user': credentials[0], 'j_password': credentials[1]})
        browser.find_by_name('uidPasswordLogon').first.click()
        if browser.is_text_present('Welcome'):
            with browser.get_iframe("ivuFrm_page0ivu1") as iframe1:  # isolatedWorkArea  ivuFrm_page0ivu4 ivuFrm_page0ivu4 sapPopupMainId_X0   obnNavIFrame externalLogOffIframe
                with iframe1.get_iframe("isolatedWorkArea") as iframe2:
                    bill_html = iframe2.html
                    # with open("origin.txt", 'w') as f:
                    #   f.write(bill)
            broswer.find_by_name('logout_submit').first.click()
        else:
            print("login was unsuccessful, try a different password")
            browser.quit()
    except: 
        browser.quit()

    soup = BeautifulSoup(bill_html)
    result = {}

    # use some variant of the "service" string to identify a link, section or page in the providers website. Here I point to the class "elec", hence service[:4].

    for service in services:
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

        result[service] = {"last_amount":last_amount, "last_date":last_date, "balance":balance, "due":due, "balance_discount":balance_discount}

    return result