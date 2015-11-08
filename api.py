# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json

apiKey = '6af9b1f2823897f75471935f92d95058'

def getAllCustomerIDs():
  url = 'http://api.reimaginebanking.com/customers/?key={}'.format(apiKey)
  response = requests.get(url)
  customers = json.loads(response.text)
  customer_ids = []
  for i in customers:
    customer_ids.append(i['_id'])
  return customer_ids

def getAllAccounts(customerID):
  url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerID, apiKey)
  response = requests.get(url)
  accounts = json.loads(response.text)
  account_ids = []
  for i in accounts:
    account_ids.append(i['_id'])
  return account_ids

def getAllPurchases(accountID):
  url = 'http://api.reimaginebanking.com/accounts/{}/purchases?key={}'.format(accountID, apiKey)
  response = requests.get(url)
  purchases = json.loads(response.text)
  return purchases
  
def getAllTransfers(accountID):
  url = 'http://api.reimaginebanking.com/accounts/{}/transfers?key={}'.format(accountID, apiKey)
  response = requests.get(url)
  transfers = json.loads(response.text)
  return transfers

def getAllWithdrawals(accountID):
  url = 'http://api.reimaginebanking.com/accounts/{}/withdrawals?key={}'.format(accountID, apiKey)
  response = requests.get(url)
  withdrawals = json.loads(response.text)
  return withdrawals

def getAllTransactions(customerID):
  accounts = getAllAccounts(customerID)
  transactions = []
  for i in accounts:
    for j in getAllPurchases(i):
      transactions.append(j)
    for j in getAllTransfers(i):
      transactions.append(j)
    for j in getAllWithdrawals(i):
      transactions.append(j)
  sorted(transactions, key=lambda transaction: transaction["date"])
  return transactions
