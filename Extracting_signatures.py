import cv2


def extractSignature(path):
    img = cv2.imread(path)  # "Original cheques/CHEQUE.png")
    # cv2.imshow('Original Image', img)
    height, width = img.shape[0:2]
    # img.shape[0:2]
    rotationMatrix = cv2.getRotationMatrix2D((width / 2, height / 2), 90, .5)
    rotatedImage = cv2.warpAffine(img, rotationMatrix, (width, height))
    # cv2.imshow('Rotated Image', rotatedImage)
    # cv2.waitKey(0)
    height, width = img.shape[0:2]
    startRow = int(height * .55)
    startCol = int(width * .55)
    endRow = int(height * .74)
    endCol = int(width * .80)
    croppedImage = img[startRow:endRow, startCol:endCol]
    # cv2.imshow('Original Image', img)
    # cv2.imshow('Cropped Image', croppedImage)
    gray_img = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
    # print(gray_img)
    # cv2.imshow("Gray Scale Image", gray_img)
    print(gray_img)
    # return(gray_img)
    cv2.imwrite("gray_img.png", gray_img)
