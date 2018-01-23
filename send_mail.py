#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 17:42:54 2018
@author: lapdog
"""

import smtplib
import logging
import requests
import time,sys


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(level=logging.DEBUG)
logging.debug('Start of program')

smtp_servers ={'gmail': {'server':'smtp.gmail.com','port':587},
'hotmail': {'server':'smtp-mail.outlook.com','port':587},
'outlook': {'server':'smtp-mail.outlook.com','port':587},
'yahoo': {'server':'smtp.mail.yahoo.com','port':587},
'att' : {'server':'smpt.mail.att.net','port':465},
'comcast' :  {'server':'smtp.comcast.net','port':587},
'verizon' :  {'server':'smtp.verizon.net','port':465},}
        
while True:
    try:
        mailProvider = input('Type in your email provider from the following:\n\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\'\n'.format(i for i in list(smtp_servers.keys())))
        user_server = smtp_servers[mailProvider]['server']
        user_port = smtp_servers[mailProvider]['port']
        break
    except KeyError:
        print('Try again')
smtpObj = smtplib.SMTP(user_server, user_port)
smtpObj.ehlo()
smtpObj.starttls()
try:
    account = input('Input your account:\n')
    password = input('Input the password for {}:\n'.format(account))
    login = smtpObj.login(account,password)
    logging.debug(login)
except Exception:
    print('Error occurred'.format(Exception))

wallets = {wallet0:False,wallet1:False}

while wallets[list(wallets.keys())[0]] == False or wallets[list(wallets.keys())[1]] == False:
    for i in wallets:
        response = requests.get('http://explorer.tpay.ai/ext/getaddress/'+i).json()
        interval = 15
        if wallets[response['hash']] == False:    
            if response['error'] == 'address not found.':
                print('No tokens received yet @ {}. Trying again in {} minutes.'.format(response['hash'],interval))
                    
            else:
                smtpObj.sendmail(account,account_to,'Subject: Your TPAY has arrived at your wallet.\nYou have received your TPAY @ {}\nSincerely,Aquaerius'.format(response['hash']))
                wallets[response['hash']] = True
            
    time.sleep(interval*60)
logout = smtpObj.quit()
if logout[0] == 221:
    print('You have been logged out of {}'.format(account))
sys.exit()   
#TODO - ask user for wallet address(es)
