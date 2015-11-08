# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json

apiKey = '6af9b1f2823897f75471935f92d95058'

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def pick_customer():
  return render_template('pick_customer.html', customers=getAllCustomers())
    
@app.route("/user/<customer_id>")
def pick_account(customer_id):
  print(customer_id)
  print(getAllAccountIDs(customer_id))
  if None:
    return "invalid customer_id"
  return render_template('pick_account.html', accounts=getAllAccounts(customer_id))
  
@app.route("/account/<account_id>")
def view_transactions(account_id):
  print(account_id)
  print('56241a13de4bf40b171129f3')
  print(getAllDeposits('56241a13de4bf40b171129f3'))
  print(account_id)
  if None:
    return "invalid customer_id"
  return render_template('view_transactions.html', transactions=getAllTransactionsForAccount(account_id))


def getAllCustomers():
  url = 'http://api.reimaginebanking.com/customers/?key={}'.format(apiKey)
  response = requests.get(url)
  customers = json.loads(response.text)
  return customers
    
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
  return accounts

def getAllAccountIDs(customerID):
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

def getAllDeposits(accountID):
  url = 'http://api.reimaginebanking.com/accounts/{}/deposits?key={}'.format(accountID, apiKey)
  response = requests.get(url)
  deposits = json.loads(response.text)
  return deposits
  
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

def getAllTransactionsForAccount(accountID):
  transactions = []
  for j in getAllPurchases(accountID):
    transactions.append(j)
  for j in getAllTransfers(accountID):
    transactions.append(j)
  for j in getAllWithdrawals(accountID):
    transactions.append(j)
  for j in getAllDeposits(accountID):
    transactions.append(j)
  sorted(transactions, key=lambda transaction: transaction["transaction_date"])
  return transactions  
  
def getAllTransactionsForCustomer(customerID):
  accounts = getAllAccountIDs(customerID)
  transactions = []
  for i in accounts:
    for j in getAllPurchases(i):
      transactions.append(j)
    for j in getAllTransfers(i):
      transactions.append(j)
    for j in getAllWithdrawals(i):
      transactions.append(j)
    for j in getAllDeposits(i):
      transactions.append(j)
  sorted(transactions, key=lambda transaction: transaction["transaction_date"])
  return transactions


if __name__ == "__main__":
    app.debug = True
    app.run()
