import sqlite3
from datetime import datetime

import extractDetails
from Extracting_signatures import extractSignature
from signatureMatching import matchSign


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month + (d1.day - d2.day) / 30.0


def processing(amountFromForm=15000, cheque='Original cheques/CHEQUE.png', bearerName='Ankit Goyal'):
    print(cheque, amountFromForm, bearerName)
    detailsFromCheque = extractDetails.extractDetailsFromCheque(cheque)
    print(detailsFromCheque)
    date = datetime.strptime(detailsFromCheque['date'], '%d/%m/%Y')

    date = date.date()
    present = datetime.now()
    present = present.date()
    # print(date, present, diff_month(present, date))
    if diff_month(present, date) > 3:
        print('E')
        return ('NAK')
    amountFromCheque = float(detailsFromCheque['amount'])
    if amountFromCheque != float(amountFromForm):
        print('F')
        return ('NAK')

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    temp = detailsFromCheque['accountNumber']
    detailsFromDB = None
    c.execute("SELECT * from ChequeClearingSystem_payeeBank where accountNumber=?", (int(temp),))
    for i in c:
        print(i)
        detailsFromDB = i
    if detailsFromDB is None:
        print('A')
        return ('NAK')
    if bearerName != detailsFromCheque['name']:
        print('Fk')
        print(bearerName)
        print(detailsFromCheque['name'])
        print('B')
        return ('NAK')

    if detailsFromDB[11] < amountFromCheque:
        print('C')
        return ('NAK')
    extractSignature(cheque)
    if not matchSign(detailsFromDB[9]):
        return ('NAK')
    print('ACK')
    return ('ACK', temp, amountFromCheque)

# processing(bearerBank.objects.filter(accountNumber=10001))
