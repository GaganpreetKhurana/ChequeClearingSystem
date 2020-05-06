import sqlite3
from datetime import datetime

import extractDetails
from ChequeClearingSystemProject.settings import BASE_DIR
from Extracting_signatures import extractSignature
from signatureMatching import matchSign
from wordToNumber import wordToNumber


def diff_month(d1, d2):
    '''
    To calculate difference between dates
    :param d1: present date
    :param d2: date on check
    :return: Difference between dates
    '''
    return (d1.year - d2.year) * 12 + d1.month - d2.month + (d1.day - d2.day) / 30.0


def processing(amountFromForm, cheque, bearerName):
    '''
    Check cheque validity and match details with the database
    :param amountFromForm: amount entered by the bearer
    :param cheque: cheque path
    :param bearerName: name of bearer
    :return: ('NAK') or
            ('ACK', temp(AccountNumber of the bearer, amountFromCheque, chequeNumber)
    '''

    # check type of parameters passed
    if not (isinstance(amountFromForm, int) or isinstance(amountFromForm, float)):
        return ("NAK")
    if not (isinstance(bearerName, str)):
        return ('NAK')

    # extract Details From Cheque
    detailsFromCheque = extractDetails.extractDetailsFromCheque(cheque)

    # connect to the database
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    temp = detailsFromCheque['accountNumber']

    # check if account Number exists in Database
    detailsFromDB = None
    c.execute("SELECT * from ChequeClearingSystem_payeeBank where accountNumber=?", (int(temp),))
    for i in c:
        detailsFromDB = i
    if detailsFromDB is None:
        return ('NAK')

    contactPayee = detailsFromDB[8]
    date = datetime.strptime(detailsFromCheque['date'], '%d/%m/%Y')
    date = date.date()
    present = datetime.now()
    present = present.date()

    # Check date validity
    if diff_month(present, date) > 3:
        return ('NAK', contactPayee, detailsFromDB[12], temp)

    # Match amount from form and cheque
    amountFromCheque = float(detailsFromCheque['amount'])
    if amountFromCheque != float(amountFromForm):
        return ('NAK', contactPayee, detailsFromDB[12], temp)

    # Cheque if cheque number is not used before
    chequeNumber = detailsFromCheque['chequeNumber']
    chequeNumber = chequeNumber.split('-')
    chequeNumber = ''.join(chequeNumber)
    c.execute("SELECT * from ChequeClearingSystem_bearerBankCheque where chequeNumber=?", (int(chequeNumber),))
    chequeNumberCheck = None
    for i in c:
        chequeNumberCheck = i
    if chequeNumberCheck is not None:
        return ("NAK", contactPayee, detailsFromDB[12], temp)

    # match bearer name
    if bearerName.lower() != detailsFromCheque['name'].lower():
        return ('NAK', contactPayee, detailsFromDB[12], temp)

    # match amount in words
    numberFromWord = wordToNumber(detailsFromCheque['amountInWords'])
    if numberFromWord != amountFromCheque:
        return ('NAK', contactPayee, detailsFromDB[12], temp)

    # cheque if amount available in payee bank
    if detailsFromDB[12] < amountFromCheque:
        return ('NAK', contactPayee, detailsFromDB[12], temp)

    # extract signature and match with database
    extractSignature(cheque)
    signPath = BASE_DIR + '/ChequeClearingSystem/files/' + detailsFromDB[10]
    if not matchSign(signPath):
        return ('NAK', contactPayee, detailsFromDB[12], temp)

    # Return positive acknowledgement
    return ('ACK', temp, amountFromCheque, chequeNumber)
