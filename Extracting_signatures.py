import cv2


def extractSignature(path):
    '''
    Extract Signature from the cheque
    :param path: path of cheque
    :return: None
    '''
    img = cv2.imread(path)
    height, width = img.shape[0:2]
    rotationMatrix = cv2.getRotationMatrix2D((width / 2, height / 2), 90, .5)
    rotatedImage = cv2.warpAffine(img, rotationMatrix, (width, height))
    height, width = img.shape[0:2]
    startRow = int(height * .55)
    startCol = int(width * .55)
    endRow = int(height * .74)
    endCol = int(width * .80)
    croppedImage = img[startRow:endRow, startCol:endCol]
    gray_img = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("gray_img.png", gray_img)
