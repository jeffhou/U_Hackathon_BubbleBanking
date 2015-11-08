# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json
import random

apiKey = '6af9b1f2823897f75471935f92d95058'

from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/populate")
def populate():
  counter = 0
  for i in getAllAccounts():
    print(counter)
    counter+=1
    
    #withdrawals
    for j in range(random.randint(3,6)):
      make_withdrawal(i["_id"], random.randint(50, 300))
    for j in range(random.randint(3,6)):
      make_deposit(i["_id"], random.randint(50, 300))
    for j in getAllAccounts():
      if i != j:
        for k in range(random.randint(0,6)):
          transfer(i["_id"], j["_id"], random.randint(20, 1000))
    
    merchants = getAllMerchants()
    random.shuffle(merchants)
    for j in merchants[:15]:
      for k in range(random.randint(0, 20)):
        purchase(i["_id"], j["_id"], random.randint(5, 300))
  return "DONE"
  
@app.route("/html")
def show_html():
  return render_template('index.html')

@app.route("/top10data")
def top10data():
  data = {"name": "Purchases", "page": "#", "children": []}
  return render_template('index.html')
  
@app.route("/")
def pick_customer():
  return render_template('pick_customer.html', customers=getAllCustomers())
    
@app.route("/user/<customer_id>")
def pick_account(customer_id):
  print(customer_id)
  print(getAllAccountIDs(customer_id))
  if None:
    return "invalid customer_id"
  return render_template('pick_account.html', accounts=getAllAccountsForCustomer(customer_id))
  
@app.route("/account/<account_id>")
def view_transactions(account_id):
  print(account_id)
  print('56241a13de4bf40b171129f3')
  print(getAllDeposits('56241a13de4bf40b171129f3'))
  print(account_id)
  if None:
    return "invalid customer_id"
  return render_template('view_transactions.html', transactions=getAllTransactionsForAccount(account_id), account_id=account_id)
  
@app.route("/accountJSON/<account_id>")
def account_json(account_id):
  data = {
      "name": getCustomerNameByAccount(account_id).split()[0], "page": url_for('pick_customer'), "x": 500, "y": 250, "amount":getAccountBalance(account_id),
      "children": [
      {"name": "Purchases", "size":50000, "x": 500, "y":590, "page": url_for('purchases_page', account_id=account_id), "amount":getPurchaseTotal(account_id)},
      {"name": "Transfers", "size": 200,"x": 900, "y":325, "page": url_for('transfers_page', account_id=account_id), "amount":getTransferTotal(account_id)},
      {"name": "Withdrawals", "size": 1000,"x": 500, "y":130, "page": url_for('withdrawals_page', account_id=account_id), "amount":getWithdrawalTotal(account_id)},
      {"name": "Deposits", "size": 200, "x": 100, "y":325, "page": url_for('deposits_page', account_id=account_id), "amount":getDepositTotal(account_id)}
      ]
      }
      #transactions=getAllTransactionsForAccount(account_id), purchaseTotal=getPurchaseTotal(account_id), depositTotal=getDepositTotal(account_id), transferTotal=getTransferTotal(account_id), withdrawal=getWithdrawalTotal(account_id)
  return json.dumps(data)
@app.route("/purchasesTop10JSON/<account_id>")
def purchases_json(account_id):
  purchases = {}
  for i in getAllPurchases(account_id):
    if i["merchant_id"] in purchases:
      purchases[i["merchant_id"]] += i["amount"]
    else:
      purchases[i["merchant_id"]] = i["amount"]
  top_purchases = []
  for i in purchases:
    top_purchases.append([i, purchases[i]])
  sorted(top_purchases, key=lambda purchase: purchase[1], reverse=True)
  
  total = 0
  for i in top_purchases[10:]:
    total += i[1]
  if total != 0:
    top_purchases = top_purchases[:10]
    top_purchases.append(['Other', total])
  for i in range(len(top_purchases)):
    if top_purchases[i][0] == 'Other':
      break
    else:
      top_purchases[i].append(top_purchases[i][0])
      top_purchases[i][0] = getMerchantName(top_purchases[i][0])
     
  data = {"name": "Purchases", "page": url_for('view_transactions', account_id = account_id), "children": [], "amount":getPurchaseTotal(account_id)}
  for i in top_purchases:
    if i[0] != 'Other':
      print(i)
      data["children"].append({"name": i[0], "size":30000, "amount":i[1], "page":url_for('specific_purchases_page', account_id=account_id, merchant_id=i[2])})
  print(data)
  return json.dumps(data)

@app.route("/transfersTop10JSON/<account_id>")
def transfers_json(account_id):
  transfers = {}
  
  for i in getAllTransfers(account_id):
    other_id = ""
    amount = 0
    
    if i["payer_id"] == account_id:
      amount = -i["amount"]
      other_id = getCustomerIdByAccount(i["payee_id"])
    else:
      amount = i["amount"]
      other_id = getCustomerIdByAccount(i["payer_id"])
      
    if other_id in transfers:
      transfers[other_id] += amount
    else:
      transfers[other_id] = amount
      
  top_transfers = []
  for i in transfers:
    top_transfers.append([i, transfers[i]])
  sorted(top_transfers, key=lambda purchase: purchase[1], reverse=True)
  
  total = 0
  for i in top_transfers[10:]:
    total += i[1]
  if total != 0:
    top_transfers = top_transfers[:10]
    top_transfers.append(['Other', total])
  for i in range(len(top_transfers)):
    if top_transfers[i][0] == 'Other':
      break
    else:
      top_transfers[i].append(top_transfers[i][0])
      top_transfers[i][0] = getCustomerName(top_transfers[i][0])
  data = {"name": "Transfers", "page": "#", "children": [], "amount":getTransferTotal(account_id)}
  for i in top_transfers:
    if i[0] != 'Other':
      print(i)
      data["children"].append({"name": i[0], "size":30000, "amount": i[1], "page":url_for('specific_transfers_page', account_id=account_id, customer_id=i[2])})
  return json.dumps(data)  
  
@app.route("/account/<account_id>/purchases")
def purchases_page(account_id):
  purchases = {}
  for i in getAllPurchases(account_id):
    if i["merchant_id"] in purchases:
      purchases[i["merchant_id"]] += i["amount"]
    else:
      purchases[i["merchant_id"]] = i["amount"]
  top_purchases = []
  for i in purchases:
    top_purchases.append([i, purchases[i]])
  sorted(top_purchases, key=lambda purchase: purchase[1], reverse=True)
  
  total = 0
  for i in top_purchases[10:]:
    total += i[1]
  if total != 0:
    top_purchases = top_purchases[:10]
    top_purchases.append(['Other', total])
  for i in range(len(top_purchases)):
    if top_purchases[i][0] == 'Other':
      break
    else:
      top_purchases[i].append(top_purchases[i][0])
      top_purchases[i][0] = getMerchantName(top_purchases[i][0])
  return render_template('top10.html', top = top_purchases, typeOfTransaction="Purchases", account_id=account_id)

@app.route("/account/<account_id>/withdrawals")
def withdrawals_page(account_id):
  withdrawals = getAllWithdrawals(account_id)
  sorted(withdrawals, key=lambda withdrawal: withdrawal["transaction_date"],reverse=True)
  return render_template('timeline.html', timeline_nodes = withdrawals, typeOfTransaction="Withdrawals", url=url_for('view_transactions', account_id=account_id))

@app.route("/account/<account_id>/deposits")
def deposits_page(account_id):
  deposits = getAllDeposits(account_id)
  sorted(deposits, key=lambda deposit: deposit["transaction_date"],reverse=True)
  return render_template('timeline.html', timeline_nodes = deposits, typeOfTransaction="Deposits", url=url_for('view_transactions', account_id=account_id))

@app.route("/account/<account_id>/transfers/<customer_id>")
def specific_transfers_page(account_id, customer_id): #actually 
  transfers = []
  for j in getAllAccountIDs(customer_id):
    if j == account_id:
      continue
    for i in getAllTransfers(account_id):
      if j == i["payer_id"]:
        transfers.append([i, False])
      if j == i["payee_id"]:
        transfers.append([i, True])
  sorted(transfers, key=lambda transfer: transfer[0]["transaction_date"],reverse=True)
  return render_template('timeline.html', timeline_nodes = transfers, typeOfTransaction="Transfers with " + getCustomerName(customer_id), url=url_for('transfers_page', account_id=account_id))

@app.route("/account/<account_id>/purchases/<merchant_id>")
def specific_purchases_page(account_id, merchant_id): #actually 
  purchases = []
  for i in getAllPurchases(account_id):
    if i["merchant_id"] == merchant_id:
      purchases.append(i)
  sorted(purchases, key=lambda transfer: transfer["purchase_date"],reverse=True)
  return render_template('timeline.html', timeline_nodes = purchases, typeOfTransaction="Purchases with " + getMerchantName(merchant_id), url=url_for('purchases_page', account_id=account_id))

@app.route("/account/<account_id>/transfers")
def transfers_page(account_id):
  transfers = {}
  
  for i in getAllTransfers(account_id):
    other_id = ""
    amount = 0
    
    if i["payer_id"] == account_id:
      amount = -i["amount"]
      other_id = getCustomerIdByAccount(i["payee_id"])
    else:
      amount = i["amount"]
      other_id = getCustomerIdByAccount(i["payer_id"])
      
    if other_id in transfers:
      transfers[other_id] += amount
    else:
      transfers[other_id] = amount
      
  top_transfers = []
  for i in transfers:
    top_transfers.append([i, transfers[i]])
  sorted(top_transfers, key=lambda purchase: purchase[1], reverse=True)
  
  total = 0
  for i in top_transfers[10:]:
    total += i[1]
  if total != 0:
    top_transfers = top_transfers[:10]
    top_transfers.append(['Other', total])
  for i in range(len(top_transfers)):
    if top_transfers[i][0] == 'Other':
      break
    else:
      top_transfers[i][0] = getCustomerName(top_transfers[i][0])
  return render_template('top10.html', top = top_transfers, typeOfTransaction="Transfers", account_id=account_id)

@app.route("/makeDeposit/<accountId>/<amt>")
def make_deposit(accountId, amt):
  url = 'http://api.reimaginebanking.com/accounts/{}/deposits?key={}'.format(accountId, apiKey)
  payload = {
    "medium": "balance",
    "transaction_date": "Sat, 07 Nov 2015 23:42:57 GMT",
    "status": "pending",
    "amount": float(amt),
    "description": "deposit"
  }
  # Create a Savings Account
  response = requests.post( 
    url, 
    data=json.dumps(payload),
    headers={'content-type':'application/json'},
    )

  if response.status_code == 201:
    return 'deposit made'
  
  else:
    return 'invalid'
@app.route("/makeWithdrawal/<accountId>/<amt>")
def make_withdrawal(accountId, amt):
  url = 'http://api.reimaginebanking.com/accounts/{}/withdrawals?key={}'.format(accountId, apiKey)
  payload = {
    "medium": "balance",
    "transaction_date": "Sat, 07 Nov 2015 23:42:57 GMT",
    "status": "pending",
    "amount": float(amt),
    "description": "withdrawal"
  }
  # Create a Savings Account
  response = requests.post( 
    url, 
    data=json.dumps(payload),
    headers={'content-type':'application/json'},
    )

  if response.status_code == 201:
    return 'withdrawal made'
  
  else:
    return 'invalid' 
@app.route("/transfer/<accountId1>/<accountId2>/<amt>")
def transfer(accountId1, accountId2, amt):
  url = 'http://api.reimaginebanking.com/accounts/{}/transfers?key={}'.format(accountId1, apiKey)
  payload = {
    "medium": "balance",
    "payee_id": accountId2,
    "amount": float(amt),
    "transaction_date": "Sat, 07 Nov 2015 23:42:57 GMT",
    "status": "pending",
    "description": "transfer"
  }
  response = requests.post( 
    url, 
    data=json.dumps(payload),
    headers={'content-type':'application/json'},
    )

  if response.status_code == 201:
    return 'transfer made'
  
  else:
    return 'invalid'
@app.route("/purchase/<accountId>/<merchantId>/<amt>")
def purchase(accountId, merchantId, amt):
  url = 'http://api.reimaginebanking.com/accounts/{}/purchases?key={}'.format(accountId, apiKey)
  payload = {
    "merchant_id": merchantId,
    "medium": "balance",
    "purchase_date": "Sat, 07 Nov 2015 23:42:57 GMT",
    "amount": float(amt),
    "status": "pending",
    "description": "purchase"
  }
  response = requests.post( 
    url, 
    data=json.dumps(payload),
    headers={'content-type':'application/json'},
    )

  if response.status_code == 201:
    return 'purchase made'
  
  else:
    return 'invalid'
def getAllCustomers():
  url = 'http://api.reimaginebanking.com/customers?key={}'.format(apiKey)
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
def getAllAccountsForCustomer(customerID):
  url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerID, apiKey)
  response = requests.get(url)
  accounts = json.loads(response.text)
  return accounts
def getAllAccounts():
  url = 'http://api.reimaginebanking.com/accounts?key={}'.format(apiKey)
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
def getPurchaseTotal(accountID):
  total = 0
  for i in getAllPurchases(accountID):
    total += i["amount"]
  return total
def getAllDeposits(accountID):
  url = 'http://api.reimaginebanking.com/accounts/{}/deposits?key={}'.format(accountID, apiKey)
  response = requests.get(url)
  deposits = json.loads(response.text)
  return deposits
def getDepositTotal(accountID):
  total = 0
  for i in getAllDeposits(accountID):
    total += i["amount"]
  return total
  
def getAllTransfers(accountID):
  url = 'http://api.reimaginebanking.com/accounts/{}/transfers?key={}'.format(accountID, apiKey)
  response = requests.get(url)
  transfers = json.loads(response.text)
  return transfers

def getTransferTotal(accountID):
  total = 0
  for i in getAllTransfers(accountID):
    total += i["amount"]
  return total
def getAllMerchants():
  url = 'http://api.reimaginebanking.com/merchants?key={}'.format(apiKey)
  response = requests.get(url)
  merchants = json.loads(response.text)
  return merchants
def getAllWithdrawals(accountID):
  url = 'http://api.reimaginebanking.com/accounts/{}/withdrawals?key={}'.format(accountID, apiKey)
  response = requests.get(url)
  withdrawals = json.loads(response.text)
  return withdrawals
  
def getWithdrawalTotal(accountID):
  total = 0
  for i in getAllWithdrawals(accountID):
    total += i["amount"]
  return total
  
def getMerchantName(merchantID):
  url = 'http://api.reimaginebanking.com/merchants/{}?key={}'.format(merchantID, apiKey)
  response = requests.get(url)
  merchant = json.loads(response.text)
  return merchant["name"]
def getAccountBalance(accountID):
  url = 'http://api.reimaginebanking.com/accounts/{}?key={}'.format(accountID, apiKey)
  response = requests.get(url)
  account = json.loads(response.text)
  return account["balance"]
def getCustomerNameByAccount(accountID):
  url = 'http://api.reimaginebanking.com/accounts/{}/customer?key={}'.format(accountID, apiKey)
  response = requests.get(url)
  customer = json.loads(response.text)
  return customer["first_name"] + " " + customer["last_name"]
def getCustomerIdByAccount(accountID):
  url = 'http://api.reimaginebanking.com/accounts/{}/customer?key={}'.format(accountID, apiKey)
  response = requests.get(url)
  customer = json.loads(response.text)
  return customer["_id"]
def getCustomerName(customerID):
  url = 'http://api.reimaginebanking.com/customers/{}?key={}'.format(customerID, apiKey)
  response = requests.get(url)
  customer = json.loads(response.text)
  print(customer)
  return customer["first_name"] + " " + customer["last_name"]
  
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
  for i in transactions:
    for j in i.keys():
      if 'date' in j:
        i["date"] = i[j]
        break
  sorted(transactions, key=lambda transaction: transaction["date"])
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
  for i in transactions:
    for j in i.keys():
      if 'date' in j:
        i["date"] = i[j]
        break
  sorted(transactions, key=lambda transaction: transaction["date"])
  return transactions


if __name__ == "__main__":
    app.debug = True
    app.run()
