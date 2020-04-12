from datetime import datetime

import requests


def sendMessage(amount, updatedBalance, contactNumber, accountNumber):
    url = "https://www.fast2sms.com/dev/bulk"
    a = "6284090494"
    transaction = ' credit '
    if amount < 0:
        transaction = ' debit '
    msg = 'Last Transaction in A/C ' + str(accountNumber) + ' at ' + str(datetime.now()) + transaction + str(
        abs(amount)) + ' Balance ' + str(updatedBalance)
    print(msg)
    msg = 'test2'
    querystring = {"authorization": "5opOL4g8RtrVU6lHMS0nWqdQfBa7jhbAJKNCZ31czFewPXvTyxHDBQVsmeRYSlT4wW8Ov9br3UpCkgIN"
        , "sender_id": "FSTSMS", "message": msg, "language": "english",
                   "route": "p", "numbers": str(contactNumber)}

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

# sendMessage(-500,4300,9815878235,123456)
