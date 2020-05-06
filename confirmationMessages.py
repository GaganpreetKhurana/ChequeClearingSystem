from datetime import datetime

import requests


def sendMessage(amount=None, updatedBalance=None, contactNumber=None, accountNumber=None, msg=None):
    '''
    To send a text message

    :param amount:amount changed
    :param updatedBalance: Final Balance
    :param contactNumber: Phone number of receiver
    :param accountNumber: account number of receiver
    :param msg: message to be sent (None for failed transaction )
    :return: None
    '''

    if contactNumber is None:
        return

    url = "https://www.fast2sms.com/dev/bulk"

    if msg is None:
        transaction = ' credit '
        if amount < 0:
            transaction = ' debit '
        msg = 'Last Transaction in A/C ' + str(accountNumber) + ' at ' + str(datetime.now()) + transaction + str(
            abs(amount)) + ' Balance ' + str(updatedBalance)

    # enter fast2sms authorization key in authorization value
    querystring = {"authorization": ""
        , "sender_id": "FSTSMS", "message": msg, "language": "english",
                   "route": "p", "numbers": str(contactNumber)}

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)
