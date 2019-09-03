import requests
import json

with open('orders.json') as json_file:
    orders = json.load(json_file)

def checkOrder(orderNum, customerNum, importantCookie, scriptStore, store):
    print("checking status of " + orderNum + " for " + store)
    session = requests.Session()

    sessionHeaders = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "content-type": "application/json"
    }

    cookies = {
        '_abck':importantCookie
    }

    s = session.get(scriptStore + 'api/session', headers=sessionHeaders, cookies=cookies)
    loadedData = json.loads(s.text)
    csrfToken = loadedData['data']['csrfToken']

    headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
    "accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "content-type": "application/json",
    "x-csrf-token":csrfToken
    }

    payload = {
        "code":orderNum,
        "customerNumber":customerNum
    }


    checkReq = session.post(scriptStore + 'api/users/orders/status', headers=headers, json=payload, cookies=cookies)

    if 200 == checkReq.status_code:
        jsonStatus = json.loads(checkReq.text)
        orderStatus1 = jsonStatus['orderStatus']
        orderStatus2 = jsonStatus['lineItems'][0]['itemStatus']

        print("status of " + orderNum + " is " + orderStatus1 + " and " + orderStatus2 + " for " + store)
    elif "match" in checkReq.text:
        print("error with order numbers or/and customer numbers, please check order numbers or/and customer numbers" + " for " + store)
        exit()
    else:
        print("cookie invalid! please get a new cookie" + " for " + store + ": ")
        importantCookie = input("please paste cookie here" + " for " + store + ": ")
        checkOrder(orderNum, cusNum, importantCookie, scriptStore, store)

def getCookie():
    global importantCookie
    firstStore  = orders["orders"][0]["store"]
    importantCookie = input("please paste cookie here" + " for " + firstStore + ": ")
getCookie()

stores = {

    "footlocker":"https://www.footlocker.com/",
    "kidsfootlocker":"https://www.kidsfootlocker.com/",
    "footaction":"https://www.footaction.com/",
    "champssports":"https://www.champssports.com/",
    "eastbay":"https://www.eastbay.com/"

}

checkStore = False

global scriptStore
global store

for i in orders["orders"]:
    orderNum = i['orderNum']
    cusNum = i['customerNum']
    store = i['store']
    for j in stores:
        if store == j:
            scriptStore = stores[j]
            checkStore = True
        elif checkStore == False and j == 4:
            print(store + " is not a valid site...please check orders.json and make sure you have the correct site")
            exit()
    checkOrder(orderNum, cusNum, importantCookie, scriptStore, store)




