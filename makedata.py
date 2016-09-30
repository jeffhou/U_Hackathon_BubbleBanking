# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json
import math
import random

apiKey = '6af9b1f2823897f75471935f92d95058'

def getAllCustomerIDs():
  url = 'http://api.reimaginebanking.com/customers/?key={}'.format(apiKey)
  response = requests.get(url)
  customers = json.loads(response.text)
  customer_ids = []
  for i in customers:
    customer_ids.append(i['_id'])
  return customer_ids

def getMerchants():
  url = 'http://api.reimaginebanking.com/merchants/?key={}'.format(apiKey)
  response = requests.get(url)
  merchants = json.loads(response.text)
  merchant_ids = []
  for i in merchants:
    merchants_ids.append(i['_id'])
  return merchants_ids

def getAllAccounts(customerID):
  url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerID, apiKey)
  response = requests.get(url)
  accounts = json.loads(response.text)
  account_ids = []
  for i in accounts:
    account_ids.append(i['_id'])
  return account_ids

def getAllAccountIDs():
        customer_ids = getAllCustomerIDs()
        AllAccountIDs = []
        for i in customer_ids:
                AllAccountIDs.append(getAllAccounts(i))
        return AllAccountIDs

def make24bit():
  answer = '';
  for j in range (1, 24):
    answer = answer + str(random.randint(0,9))
  return answer

def makeCustomerIDs(num_customers):
  customer_ids = []
  for i in range (1, num_customers+1):
    temp = make24bit()
    customer_ids.append(temp)
  return customer_ids

def makeMerchantIDs(num_merchants):
  merchant_ids = []
  for i in range (1, num_merchants+1):
    temp = make24bit()
    merchant_ids.append(temp)
  return merchant_ids

def makeAccountIDs(customer_ids):
  account_ids = dict()
  for i in customer_ids:
    numaccounts = random.randint(1,4)
    temp = []
    for j in range(1,numaccounts):
      temp.append(make24bit())
    account_ids[i] = temp
  return account_ids



testCustomerIDs = makeCustomerIDs(10)
testMerchantIDs = makeMerchantIDs(10)
testAccountIDs = makeAccountIDs(testCustomerIDs)
testDeposits = makeDeposits(testAccountIDs)
testTransfers = makeTransfers(testAccountIDs)
testPurchases = makePurchases(testAccountIDs,testMerchantIDs)
print(testCustomerIDs)
print(testMerchantIDs)
print(testAccountIDs)
