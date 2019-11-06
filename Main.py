import cv2 as cv, numpy as np

# hello this is a test comment

def show_webcam(mirror=False):
    cam = cv.VideoCapture(0)
    background = None

    while True:
        ret_val, img = cam.read()

        if mirror:
            img = cv.flip(img, 1)

        #Filters
        img_analyze = img.copy()
        img_analyze = cv.medianBlur(img_analyze, 3)
        img_analyze = cv.cvtColor(img_analyze, cv.COLOR_BGR2GRAY)

        if background is not None:
            img_analyze = cv.subtract(background, img_analyze)


        # #Detection Box
        win_w = len(img_analyze[0])
        win_h = len(img_analyze)
        pad_x = 200
        pad_y = 100
        cv.rectangle(img_analyze, (0, 0), (pad_x, win_h), (0, 0, 0), thickness=-1)
        cv.rectangle(img_analyze, (pad_x, 0), (win_w-pad_x, pad_y), (0, 0, 0), thickness=-1)
        cv.rectangle(img_analyze, (win_w-pad_x, 0), (win_w, win_h), (0, 0, 0), thickness=-1)
        cv.rectangle(img_analyze, (pad_x, win_h-pad_y), (win_w-pad_x, win_h), (0, 0, 0), thickness=-1)

        #Contour Detection
        ret, thresh = cv.threshold(img_analyze, 127, 255, cv.THRESH_BINARY)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        #Drawing Contours
        cv.drawContours(img, contours, -1, (0,255,0), 3)

        cv.imshow("Whiteboard Game", img)

        k = cv.waitKey(1)

        if k == 27:
            break
        elif k == 32:
            background = img_analyze.copy()

    cv.destroyAllWindows()

def main():
    show_webcam(True)


if __name__ == '__main__':
    main()