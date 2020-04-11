from PIL import Image
import pytesseract as pt
pt.pytesseract.tesseract_cmd=r'C:\Users\AKSHIT\AppData\Local\Programs\Python\Python37-32\Scripts\Tesseract.exe'
im=Image.open("CHEQUE.png")
text=pt.image_to_string(im)
data=text.splitlines( )
#print(data)
BANK_NAME=data[0]
IFSC=""
DATE=""
BEARER_FNAME=""
BEARER_LNAME=""
AMOUNT=""
ACC_NO=""
CHEQUE_NO=data[-1]
for x in data:
    y=x.split()
    for index,z in enumerate(y):
        if z=='IFSC':
            IFSC=y[index+1]
            #print("IFSC",IFSC)
        if z=='DATE:':
            DATE=y[index+1]
            #print("DATE",DATE)
        if z=='Pay:':
            BEARER_FNAME=y[index+1]
            BEARER_LNAME=y[index+2]
            #print("BEARER_FNAME",BEARER_FNAME)
            #print("BEARER_LNAME",BEARER_LNAME)
        if z=='RS:':
            AMOUNT=y[index+1]
            #print("AMOUNT",AMOUNT)
        if z=='No.':
            ACC_NO=y[index+1]
            #print("ACC_NO",ACC_NO)
#print("CHEQUE_NO",CHEQUE_NO)
#print("BANK_NAME",BANK_NAME)
return(IFSC,DATE,BEARER_FNAME,BEARER_LNAME,AMOUNT,ACC_NO,CHEQUE_NO,BANK_NAME)
