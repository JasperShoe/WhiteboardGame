import cv2 as cv, numpy as np


def show_webcam(mirror=False):
    cam = cv.VideoCapture(0)

    while True:
        ret_val, img = cam.read()

        if mirror:
            img = cv.flip(img, 1)

        #output = img.copy()
        # img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # img = cv.medianBlur(img, 3)
        # img = cv.Canny(img, 100, 150)

        img = cv.medianBlur(img, 3)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY)
        img_inv = cv.bitwise_not(img_gray)


        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(img_inv, contours, -1, (0,255,0), 3)

        cv.imshow("Whiteboard Game", img_inv)

        # lines = cv.HoughLinesP(img, 1, np.pi/180, threshold = 100, minLineLength = 10, maxLineGap = 50)
        # if lines is not None:
        #     for line in lines:
        #         x1, y1, x2, y2 = line[0]
        #         cv.line(output, (x1, y1), (x2, y2), (255, 0, 0), 3)
        #cv.rectangle(output, (100, 100), (1180, 620), (0, 0, 255), 2)

       # cv.imshow('Whiteboard Game', img)
        if cv.waitKey(1) == 27:
            break

    cv.destroyAllWindows()

def main():
    show_webcam(True)


if __name__ == '__main__':
    main()