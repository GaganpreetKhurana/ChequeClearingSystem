import cv2


def matchSign(fromDB, fromCheque='gray_img.png'):
    '''
    match signature with the Database
    :param fromDB: path of signature from Database
    :param fromCheque: extracted signature
    :return: bool (Matched or Not)
    '''
    original = cv2.imread(fromDB)
    duplicate = cv2.imread(fromCheque)
    difference = cv2.subtract(original, duplicate)
    b, g, r = cv2.split(difference)
    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        return True
    else:
        return False
