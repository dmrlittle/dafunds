# -*- coding: utf-8 -*-

import requests
import json

# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
import paytmchecksum

def initiatepay(tmid,torderId,tmkey,tcallbackUrl):
    paytmParams = dict()
    
    paytmParams["body"] = {
    "requestType"   : "Payment",
    "mid"           : tmid ,
    "websiteName"   : "DAFunds",
    "orderId"       : torderId ,
    "callbackUrl"   : tcallbackUrl,
    "txnAmount"     : { "value"     : "1.00",
                       "currency"  : "INR"},
    "userInfo"      : {"custId"    : "CUST_001"}
    }
    
    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    checksum = paytmchecksum.generateSignature(json.dumps(paytmParams["body"]),tmkey)

    paytmParams["head"] = { "signature"    : checksum }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = f"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={tmid}&orderId={torderId}"
    
    # for Production
    # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
    
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    
    return response,checksum

def genotp(tmid,torderId,ttxnToken,tmobileNo):
    paytmParams = dict()

    paytmParams["body"] = { "mobileNumber" : tmobileNo }

    paytmParams["head"] = { "txnToken"     : ttxnToken }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = f"https://securegw-stage.paytm.in/login/sendOtp?mid={tmid}&orderId={torderId}"
    
    # for Production
    # url = "https://securegw.paytm.in/login/sendOtp?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
    
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    
    return response

def validateotp(tmid,torderId,ttxnToken,totp):
    paytmParams = dict()

    paytmParams["body"] = { "otp"      : totp }
    
    paytmParams["head"] = { "txnToken" : ttxnToken }
    
    post_data = json.dumps(paytmParams)
    
    # for Staging
    url = f"https://securegw-stage.paytm.in/login/validateOtp?mid={tmid}&orderId={torderId}"
    
    # for Production
    # url = "https://securegw.paytm.in/login/validateOtp?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
    
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    
    return response

def validatevpa(tmid,torderId,ttxnToken,tvpa):
    paytmParams = dict()

    paytmParams["body"] = {
        "vpa"      : tvpa
    }
    
    paytmParams["head"] = {
        "tokenType"     : "TXN_TOKEN",
        "token"         : ttxnToken
    }
    
    post_data = json.dumps(paytmParams)
    
    # for Staging
    url = f"https://securegw-stage.paytm.in/theia/api/v1/vpa/validate?mid={tmid}&orderId={torderId}"
    
    # for Production
    # url = "https://securegw.paytm.in/theia/api/v1/vpa/validate?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
    
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    
    return response

def processpay(tmid,torderID,ttxnToken,tvpa):
    paytmParams = dict()

    paytmParams["body"] = {
        "requestType" : "NATIVE",
        "mid"         : tmid,
        "orderId"     : torderID,
        "paymentMode" : "UPI",
        "channelCode" : "collect",
        "payerAccount": tvpa
    }
    
    paytmParams["head"] = {
        "txnToken"    : ttxnToken
    }
    
    post_data = json.dumps(paytmParams)
    
    # for Staging
    url = f"https://securegw-stage.paytm.in/theia/api/v1/processTransaction?mid={tmid}&orderId=torderId"
    
    # for Production
    # url = "https://securegw.paytm.in/theia/api/v1/processTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
    
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    
    return response   

def paystatus(tmid,torderId,tmkey):
    paytmParams = dict()

    # body parameters
    paytmParams["body"] = {
    
        # Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
        "mid" : tmid,
    
        # Enter your order id which needs to be check status for
        "orderId" : torderId,
    }
    
    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    checksum = paytmchecksum.generateSignature(json.dumps(paytmParams["body"]), tmkey)
    
    # head parameters
    paytmParams["head"] = {
    
        # put generated checksum value here
        "signature"	: checksum
    }
    
    # prepare JSON string for request
    post_data = json.dumps(paytmParams)
    
    # for Staging
    url = "https://securegw-stage.paytm.in/v3/order/status"
    
    # for Production
    # url = "https://securegw.paytm.in/v3/order/status"
    
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()

    return response

mid="BcQNyT61707278565114"
orderId="ORDERID_12"