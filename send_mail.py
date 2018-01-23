#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 17:42:54 2018
@author: lapdog
"""

import smtplib
import logging
import requests
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(level=logging.DEBUG)
logging.debug('Start of program')

# ------------SENSITIVE INFO - REMOVE BEFORE SHARING --------------------------

wallets_dict = {}
accounts = {'from':[],'to':[]}

# ------------SENSITIVE INFO - REMOVE BEFORE SHARING -^-^-^--------------------

check_interval = 60

smtp_servers ={'gmail': {'server':'smtp.gmail.com','port':587},
'hotmail': {'server':'smtp-mail.outlook.com','port':587},
'outlook': {'server':'smtp-mail.outlook.com','port':587},
'yahoo': {'server':'smtp.mail.yahoo.com','port':587},
'att' : {'server':'smpt.mail.att.net','port':465},
'comcast' :  {'server':'smtp.comcast.net','port':587},
'verizon' :  {'server':'smtp.verizon.net','port':465},}


print('This program will notify by email when your TPAY wallet has been credited with tokens, and the balance.')
while True:
    try:
        mailProvider = input('Type in your email provider from the following:\n\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\'\n' % tuple(smtp_servers.keys()))
        user_server = smtp_servers[mailProvider]['server']
        user_port = smtp_servers[mailProvider]['port']
        break
    except KeyError:
        print('Please try again.')
smtpObj = smtplib.SMTP(user_server, user_port)
smtpObj.ehlo()
smtpObj.starttls()

try:
    accounts['from']= input('Input your account:\n')
    password = input('Input the password for {}:\n'.format(accounts['from']))
    login = smtpObj.login(accounts['from'],password)
    logging.debug(login)
    accounts['to'].append(input('Input the email addresses where you want to be notified,\nseparated by a comma ",":\n').split(','))
    wallets = input('Input the wallets you want to check separated by a comma ",":\n').split(',')
    check_interval = int(input('How often do you want to check these wallets ? In minutes:\n'))
    for i in wallets:
        wallets_dict[i] = False
        
except Exception as e:
    print(str(e))

while any(value == False for key, value in wallets_dict.items()): 
    for i in wallets_dict:
        response = requests.get('http://explorer.tpay.ai/ext/getaddress/'+i).json()
        if wallets_dict[response['hash']] == False:    
            if response['error'] == 'address not found.':
                print('No tokens received yet in wallet: {}.\nTrying again in {} minutes.'.format(response['hash'],check_interval))
            else:
                balance = requests.get('http://explorer.tpay.ai/ext/getbalance/'+i).json()
                smtpObj.sendmail(accounts['from'],','.join(accounts['to']),'Subject: Your TPAY has arrived at your wallet.\nYou have received your {} TPAY in {}\nSincerely,Aquaerius'.format(balance,response['hash']))
                wallets_dict[response['hash']] = True
            
    time.sleep(check_interval*60)
logout = smtpObj.quit()
if logout[0] == 221:
    print('You have been logged out of {}'.format(accounts['from']))

