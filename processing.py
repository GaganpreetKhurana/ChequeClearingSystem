import sqlite3
from datetime import datetime

import extractDetails
from ChequeClearingSystemProject.settings import BASE_DIR
from Extracting_signatures import extractSignature
from signatureMatching import matchSign


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month + (d1.day - d2.day) / 30.0


def processing(amountFromForm, cheque, bearerName):
    if not (isinstance(amountFromForm, int) or isinstance(amountFromForm, float)):
        return ("NAK")
    if not (isinstance(bearerName, str)):
        return ('NAK')
    detailsFromCheque = extractDetails.extractDetailsFromCheque(cheque)
    date = datetime.strptime(detailsFromCheque['date'], '%d/%m/%Y')

    date = date.date()
    present = datetime.now()
    present = present.date()
    if diff_month(present, date) > 3:
        return ('NAK')
    amountFromCheque = float(detailsFromCheque['amount'])
    if amountFromCheque != float(amountFromForm):
        return ('NAK')

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    chequeNumber = detailsFromCheque['chequeNumber']
    chequeNumber = chequeNumber.split('-')
    chequeNumber = ''.join(chequeNumber)
    c.execute("SELECT * from ChequeClearingSystem_bearerBankCheque where accountNumber=?", (int(chequeNumber),))
    chequeNumberCheck = None
    for i in c:
        chequeNumberCheck = i
    if chequeNumberCheck is not None:
        return ("NAK")

    temp = detailsFromCheque['accountNumber']
    detailsFromDB = None
    c.execute("SELECT * from ChequeClearingSystem_payeeBank where accountNumber=?", (int(temp),))
    for i in c:
        detailsFromDB = i
    if detailsFromDB is None:
        return ('NAK')
    if bearerName != detailsFromCheque['name']:
        return ('NAK')

    if detailsFromDB[11] < amountFromCheque:
        return ('NAK')
    extractSignature(cheque)
    signPath = BASE_DIR + '/ChequeClearingSystem/files/' + detailsFromDB[9]
    if not matchSign(signPath):
        return ('NAK')
    return ('ACK', temp, amountFromCheque, chequeNumber)
