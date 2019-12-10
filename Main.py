import cv2 as cv, numpy as np
import Game as game
from multiprocessing import Process
import threading
import math


# hello this is a test comment


def show_webcam(mirror=False):
    cam = cv.VideoCapture(0)
    # cam.set(cv.CAP_PROP_EXPOSURE, 10)
    background = None
    xStart = []
    yStart = []
    xEnd = []
    yEnd = []

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
        cv.rectangle(img_analyze, (0, 0), (10, win_h), (0, 0, 0), thickness=-1)
        cv.rectangle(img_analyze, (10, 0), (win_w-500, pad_y), (0, 0, 0), thickness=-1)
        cv.rectangle(img_analyze, (win_w-500, 0), (win_w, win_h), (0, 0, 0), thickness=-1)
        cv.rectangle(img_analyze, (10, win_h-pad_y), (win_w-500, win_h), (0, 0, 0), thickness=-1)

        #Contour Detection
        ret, thresh = cv.threshold(img_analyze, 127, 255, cv.THRESH_BINARY)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        for i in range(len(xStart)):
            cv.line(img, (xStart[i],yStart[i]), (xEnd[i],yEnd[i]), (0, 255, 0), 5)

            # draw contour on the screen
             #Drawing Contours
        # cv.drawContours(img, contours, -1, (0,255,0), 3)
        #
        # cv.imshow("Whiteboard Game", img)
        # cv.moveWindow("Whiteboard Game", 0, 0)

        k = cv.waitKey(1)


        if k == 27:
            break
        elif k == 32: #spacebar zeroes contours
            background = img_analyze.copy()
        elif k == ord('d'): #gets the arrays of start/ending x/y coords
            xStart = []
            yStart = []
            xEnd = []
            yEnd = []

            x = []
            y = []
            for i in range(0,len(contours)):
                for r in range(len(contours[i])):
                    x.append(contours[i][r][0][0])
                    y.append(contours[i][r][0][1])

                if not min(x) == 11 and not y[np.where(x==min(x))[0][0]] == 101 or not max(x) == 779 and not y[np.where(x==max(x))[0][0]] == 619:
                    xStart.append(min(x))
                    z = np.where(x==min(x))
                    z = z[0][0]

                    yStart.append(y[z])


                    xEnd.append(max(x))
                    z = np.where(x==max(x))


                    z = z[0][0]

                    yEnd.append(y[z])




                #draw contour on the screen
                    cv.line(img, (x[0], y[0]), (x[len(x)-1], y[len(y)-1]), (0, 255, 0), 5)

                x = []
                y = []


            # print(xStart)
            # print(yStart)
            # print(len(xStart))
            # print(len(yStart))
            #
            #
            # #print("test")
            # print(xEnd)
            # print(yEnd)
            # print(len(xEnd))
            # print(len(yEnd))
            # print(len(contours))
        center = (int(game.player.x), int(game.player.y))
        cv.circle(img, center, game.player.size, (255, 0, 0))

    cv.destroyAllWindows()

def main():
    show_webcam(True)
    # print("hi")


if __name__ == '__main__':
    main()
    #
    # t1 = threading.Thread(target=show_webcam(True), args=())
    # # t2 = threading.Thread(target=game.Game(), args=())
    # t2.start()
    # t1.start()
    # t1.join()
    # t2.join()


    # p = Process(target=game.Game())
    # p2 = Process(target=main())
    # p.start()
    # p2.start()