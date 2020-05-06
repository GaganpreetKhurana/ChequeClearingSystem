import pytesseract as pt
from PIL import Image


# pt.pytesseract.tesseract_cmd=r'C:\Users\AKSHIT\AppData\Local\Programs\Python\Python37-32\Scripts\Tesseract.exe'
def extractDetailsFromCheque(filePath):
    '''
    To extract details from the cheque
    :param filePath: path of Cheque
    :return: Dictionary of details extracted
                amountInWords
                bankName
                chequeNumber
                ifsc
                date
                name(bearer)
                amount
                accountNumber
    '''
    im = Image.open(filePath)
    text = pt.image_to_string(im)
    data = text.splitlines()
    details = dict()
    temp = data[8].split()[1:]
    details['amountInWords'] = ''
    for i in temp:
        details['amountInWords'] += i + ' '
    details['amountInWords'] = details['amountInWords'][:-1]

    details['bankName'] = data[0]
    details['chequeNumber'] = data[-1]
    for x in data:
        y = x.split()
        for index, z in enumerate(y):
            if z == 'IFSC':
                details['ifsc'] = y[index + 1]
            if z == 'DATE:':
                details['date'] = y[index + 1]
            if z == 'Pay:':
                details['name'] = y[index + 1] + ' ' + y[index + 2]
            if z == 'RS:':
                details['amount'] = y[index + 1]
            if z == 'No.':
                details['accountNumber'] = y[index + 1]
    return details
