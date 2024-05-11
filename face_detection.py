import cv2 as cv


def find_face(image):
    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    faces = cv.CascadeClassifier('faces.xml')

    results = faces.detectMultiScale(gray, scaleFactor=1.01, minNeighbors=4)

    for (x, y, w, h) in results:
        cv.rectangle(img, (x, y), (x + w, y + h), (255, 0), thickness=3)

    return img
    cv.waitKey(0)
