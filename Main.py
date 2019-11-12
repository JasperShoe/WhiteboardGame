import cv2 as cv, numpy as np


def show_webcam(mirror=False):
    imgAnalyzeCreated = False
    cam = cv.VideoCapture(0)
    background = None
    checkImages = True

    while True:
        ret_val, img = cam.read()

        if not imgAnalyzeCreated:
            img_analyze = img.copy()
            imgAnalyzeCreated = True

        if mirror:
            img = cv.flip(img, 1)


        if checkImages:
            # Filters
            img_analyze = img.copy()
            # set pixels to white or black
            for r in range(len(img_analyze)):
                for c in range(len(img_analyze[0])):
                    total = 0
                    for x in range(2):
                        total += img_analyze[r][c][x]
                    if total > 100:
                        img_analyze[r][c] = (1, 1, 1)
                    else:
                        img_analyze[r][c] = (255, 255, 255)

        img_analyze = cv.medianBlur(img_analyze, 3)
        img_analyze = img_analyze.astype('uint16')
        img_analyze = cv.cvtColor(img_analyze, cv.COLOR_RGB2GRAY)
        # if background is not None:
        #     img_analyze = cv.subtract(background, img_analyze)

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
        img_analyze = img_analyze.astype('uint8')
        img_analyze = cv.Canny(img_analyze, 0.0, 0.0, int(5), False)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        #Drawing Contours
        cv.drawContours(img, contours, -1, (0,255,0), 3)

        cv.imshow("Whiteboard Game", img_analyze)

        k = cv.waitKey(1)

        if k == 27:
            break
        elif k == 32:
            background = img_analyze.copy()
        elif k == ord('p'):
           checkImages = True
        else:
            checkImages = False


    cv.destroyAllWindows()

def main():
    show_webcam(True)


if __name__ == '__main__':
    main()