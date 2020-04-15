import sqlite3
from datetime import datetime

import extractDetails
from ChequeClearingSystemProject.settings import BASE_DIR
from Extracting_signatures import extractSignature
from signatureMatching import matchSign
from wordToNumber import wordToNumber


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month + (d1.day - d2.day) / 30.0


def processing(amountFromForm, cheque, bearerName):
    if not (isinstance(amountFromForm, int) or isinstance(amountFromForm, float)):
        return ("NAK")
    if not (isinstance(bearerName, str)):
        return ('NAK')
    detailsFromCheque = extractDetails.extractDetailsFromCheque(cheque)
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    temp = detailsFromCheque['accountNumber']
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
    if diff_month(present, date) > 3:
        return ('NAK', contactPayee, detailsFromDB[12], temp)
    amountFromCheque = float(detailsFromCheque['amount'])
    if amountFromCheque != float(amountFromForm):
        return ('NAK', contactPayee, detailsFromDB[12], temp)

    chequeNumber = detailsFromCheque['chequeNumber']
    chequeNumber = chequeNumber.split('-')
    chequeNumber = ''.join(chequeNumber)
    c.execute("SELECT * from ChequeClearingSystem_bearerBankCheque where chequeNumber=?", (int(chequeNumber),))
    chequeNumberCheck = None
    for i in c:
        chequeNumberCheck = i
    if chequeNumberCheck is not None:
        return ("NAK", contactPayee, detailsFromDB[12], temp)

    if bearerName.lower() != detailsFromCheque['name'].lower():
        return ('NAK', contactPayee, detailsFromDB[12], temp)
    numberFromWord = wordToNumber(detailsFromCheque['amountInWords'])
    if numberFromWord != amountFromCheque:
        return ('NAK', contactPayee, detailsFromDB[12], temp)
    if detailsFromDB[12] < amountFromCheque:
        return ('NAK', contactPayee, detailsFromDB[12], temp)
    extractSignature(cheque)
    signPath = BASE_DIR + '/ChequeClearingSystem/files/' + detailsFromDB[10]
    if not matchSign(signPath):
        return ('NAK', contactPayee, detailsFromDB[12], temp)
    return ('ACK', temp, amountFromCheque, chequeNumber)

