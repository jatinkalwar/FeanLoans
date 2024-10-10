import time
import datetime
from urllib.parse import urlparse, parse_qs, unquote, quote
import requests
from bs4 import BeautifulSoup
from starlette.responses import JSONResponse

from codes.Models import users, amount, transactiondb, forms
from codes.extra import transaction_token

USER_TOKEN = "994839198a4b6514dc9cc296c3bda19c"
MONEY_NOTIFICATION = "rs added to your wallet successfully"

async def createorder(applicationid , token , type):
    try:
        gplink = users.find_one({"token": token},
                                      {'mobile': 1, '_id': 0})
        if gplink is None:
            return JSONResponse(status_code=200,
                                content={"success": False, "message": "No User Found"})

        transaction_code = f"0706{transaction_token()}"
        finddata = amount.find_one({"payment": "allpayment"},
                                   {'form_charge': 1, '_id': 0})
        global amounts
        if type=="1":
            amounts = "1"
            # amounts =  finddata['form_charge']
        orderapi = await create_antipay(amounts , transaction_code , token)
        if orderapi["status"] is True:
            transactiondb.insert_one(
                {"token": token, "paid": False, "date": get_formatted_datetime(), "mobile": gplink['mobile'],
                 "wallet_add": False, "amount":amounts, "transaction_id": transaction_code, "complete_date": "",
                 "utr": "", "payment_url": orderapi['result']['payment_url'] , "application": applicationid})
            link = await payment_qr(orderapi['result']['payment_url'])
            upic = await getdata(link)
            if upic is False:
                return JSONResponse(status_code=200,
                                    content={"success": False, "message": "UPI Link Error"})

            return JSONResponse(status_code=200, content={"success": True, "message": "Transaction Initiate" , "qr_code": link , "upi": upic , "orderid": transaction_code})

        else:

            return JSONResponse(status_code=200, content={"success": False, "message": "Something Went Wrong"})

    except Exception as e:
        print(e)
        return JSONResponse(status_code=200, content={"success": False, "message": "Something Went Wrong"})


async def getstatus(transaction):
    try:
        datas = await getBtyeid(transaction)

        if datas["status"] == "fail":
            return JSONResponse(status_code=200, content={"success": False, "message": "order not found"})

        sta = await  getendstatus(datas['byteTransactionId'])
        if sta == "Payment pendingPENDING":
            return JSONResponse(status_code=200, content={"success": False, "message": "Pending"})
        elif sta == "fraud":

            return JSONResponse(status_code=200, content={"success": False, "message": "mismatch"})
        elif sta == "success":
            print(transaction)
            gplink = transactiondb.find_one({"transaction_id": transaction},{'wallet_add': 1, 'paid': 1, '_id': 0 , 'amount': 1 , 'token': 1})

            if gplink['wallet_add'] is False:
                res = await getutr(transaction)

                if res['status']  is True:
                    if res['result']['status'] == 'SUCCESS':
                        # data = forms.find_one({"token": gplink['token']},
                        #                   {'amount_paid': 1, '_id': 0})

                        transactiondb.update_one({"transaction_id": transaction},
                                               {"$set": {"wallet_add": True , 'paid': True , 'utr':res['result']['utr'] ,  'complete_date': get_formatted_datetime() }})
                        forms.update_one({"token": gplink['token']},
                                              {"$set": {"amount_paid": True}})
                        # await sendnotification(gplink['deviceid'] , f"{res['result']['amount']}{MONEY_NOTIFICATION}" )
                        # await updatetransactionforus(gplink['deviceid'] , "Add Money Through Anitoolz Gateway" ,gplink['amount'] , "0"  , str(int(data['wallet']) + res['result']['amount']) , await genratetransactionid() )
                        return JSONResponse(status_code=200, content={"success": True, "message": "Payment Paid"})
            return JSONResponse(status_code=200, content={"success": False, "message": "Something Went Wrong"})
        elif sta == "Order already processed":
            return JSONResponse(status_code=200, content={"success": True, "message": "Payment Already Paid"})
        else:
            return JSONResponse(status_code=200, content={"success": False, "message": "Something Went Wrong"})

    except Exception as e:
        print(e)
        return JSONResponse(status_code=200, content={"success": False, "message": "Something Went Wrong"})

async def orderapi(orderid):
    url = "https://antitest.web24.site/api/check-order-status"
    datas = {
    "user_token": USER_TOKEN,
    "order_id": orderid
}

    res =  requests.post(url , datas)
    return res.json()

def generate_random_code():
    time_part = int(time.time() * 1000)
    date_part = datetime.datetime.now().strftime("%Y%m%d")
    random_code = f"{time_part}{date_part}"
    return random_code

async def getutr(transacion):
    url = 'https://antitest.web24.site/api/check-order-status'
    data= {
    "user_token": USER_TOKEN,
    "order_id": transacion
}
    res = requests.post(url , data=data)
    return res.json()

async def getBtyeid(orderid):
    res =  requests.get(f"https://antitest.web24.site/get_byte_transaction_id.php?order_id={orderid}")
    return res.json()

async def getendstatus(byteid):
    try:

        url = "https://antitest.web24.site/order3/payment-status"
        datas = {
            'byte_order_status': byteid
        }

        res = requests.post(url , data=datas)

        return  res.text
    except Exception as e:
        print(e)
        return "fail"


async def create_antipay(wallet , transaction , token, ):
    datas = {
        "customer_mobile": token,
        "user_token": USER_TOKEN,
        "amount": wallet,
        "order_id": transaction,
        "redirect_url": "https://antitest.web24.site/success",
        "remark1": "test1",
        "remark2": "test2"

    }
    response = requests.post("https://antitest.web24.site/api/create-order", data=datas)
    return response.json()


def get_formatted_datetime():
    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%d %B %Y %I:%M %p")


    return formatted_datetime


async def payment_qr(url):
    new = url.replace("\\/", "/")
    response = requests.get(new)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the webpage content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the image element with the desired URL
        img_tag = soup.find('img', src=True)

        # Check if the image tag exists and print the URL
        if img_tag:
            image_url = img_tag['src']
            return image_url
        else:
            return False
    else:
        return False

def getdirect(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Get the 'data' parameter value
    data_value = query_params.get('data', [None])[0]
    return quote(data_value)

async def getdata(url):
    parsed_url = urlparse(url)

    # Extract the 'data' parameter from the query string
    query_params = parse_qs(parsed_url.query)
    if 'data' in query_params:
        # The 'data' parameter is URL-encoded, so we decode it
        encoded_data = query_params['data'][0]
        decoded_data = unquote(encoded_data)
        return decoded_data
    else:
        return False


