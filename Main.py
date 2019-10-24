
import cv2


def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)

        cv2.rectangle(img, (50, 50), (1230, 670), (0, 0, 255), 5)

        rows = len(img)
        cols = len(img[0])

        for r in range(rows):
            for c in range(cols):
                if(img[r][c])

        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()

    #comment