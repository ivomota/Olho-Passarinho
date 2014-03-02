import cv2

img  = cv2.imread("img/347036227091968000.JPEG")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("gray.jpg", gray)

