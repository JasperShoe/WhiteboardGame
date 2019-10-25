import cv2 as cv, numpy as np


def show_webcam(mirror=False):
    cam = cv.VideoCapture(0)
    while True:
        ret_val, img = cam.read()

        if mirror:
            img = cv.flip(img, 1)

        output = img.copy()

        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = cv.medianBlur(img, 5)
        img = cv.Canny(img, 75, 150)

        circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 200, param1=100, param2=20, minRadius=1, maxRadius=100)
        circles = np.uint16(np.around(circles))
        for(x, y, r) in circles[0, :]:
            cv.circle(output, (x, y), r, (0, 255, 0), 3)
            cv.circle(output, (x, y), 2, (0, 255, 0), 3)

        cv.rectangle(output, (100, 100), (1180, 620), (0,0,255), 2)

        cv.imshow('Whiteboard Game', output)

        #cv.imshow('Whiteboard Game', img)


        if cv.waitKey(1) == 27:
                break

    cv.destroyAllWindows()

def main():
    show_webcam(True)


if __name__ == '__main__':
    main()