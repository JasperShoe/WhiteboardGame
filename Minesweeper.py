import pygame
from pygame.locals import *
import cv2 as cv
import numpy as np
import sys
import random
import math

camera = cv.VideoCapture(0)
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
screen = pygame.display.set_mode([1280, 720])

drag = 0.999
elasticity = 0.75
gravity = (math.pi, 0.005)
touching = False

img = None


background = None
xStart = []
yStart = []
xEnd = []
yEnd = []

def getImg():
    global xStart, yStart, xEnd, yEnd
    ret_val, img = camera.read()

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

    # img = cv.flip(img, 1)

    #Contour Detection
    ret, thresh = cv.threshold(img_analyze, 127, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # for i in range(len(xStart)):
    #     cv.line(img, (xStart[i],yStart[i]), (xEnd[i],yEnd[i]), (0, 255, 0), 5)

        # draw contour on the screen
         #Drawing Contours
    cv.drawContours(img, contours, -1, (0,255,0), 3)
    #
    # cv.imshow("Whiteboard Game", img)
    # cv.moveWindow("Whiteboard Game", 0, 0)

    k = cv.waitKey(1)

    # if k == 27:
    #     break
    # elif k == 32: #spacebar zeroes contours
    #     background = img_analyze.copy()
    if k == ord('d'): #gets the arrays of start/ending x/y coords
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
    return img

def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)
    return (angle, length)


def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x - x, p.y - y) <= p.size:
            return p
    return None


def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent

        angle1 = 2 * tangent - p1.angle
        angle2 = 2 * tangent - p2.angle
        speed1 = p2.speed * elasticity
        speed2 = p1.speed * elasticity

        (p1.angle, p1.speed) = (angle1, speed1)
        (p2.angle, p2.speed) = (angle2, speed2)

        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)


def collideLine(particle, line): #checks if particle is touching a line
    touching = False
    px = particle.x
    py = particle.y

    xstart = line.xstart
    ystart = line.ystart
    xend = line.xend
    yend = line.yend

    pygame.draw.polygon(screen, (0, 0, 0), [[px, py], [xstart, ystart], [xend, yend]], 5)

    side1 = math.sqrt(((xstart-px)*(xstart-px))+((ystart-py)*(ystart-py)))
    side2 = math.sqrt(((xend-xstart)*(xend-xstart))+((yend-ystart)*(yend-ystart)))
    side3 = math.sqrt(((xend - px) * (xend - px)) + ((yend - py) * (yend - py)))

    semi = int((side1+side2+side3)/2)

    area = math.sqrt(abs((semi)*(semi-side1)*(semi-side2)*(semi-side3)))

    # print(px)

    height = int((2*area)/side2)
    if px < xend and px > xstart: #checks if particle is actually colliding with line and not a ghost line

        if height <= particle.size:
            touching = True
            # print(area)
            #
            # print ("works")
            # #print(height)

    #
        if touching == True: #computes the particle's new direction
            lineXCompenent = line.xend - line.xstart
            lineYCompenent = line.yend - line.ystart
            lineAngle = math.degrees(math.atan(lineYCompenent/lineXCompenent))

            particleAngle = math.degrees(particle.angle)

            angleDifferences = particleAngle - lineAngle
            newAngle = 180 + lineAngle - particleAngle
            particle.angle = math.radians(newAngle)
            return True
        return False


class Particle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.angle, self.speed) = addVectors(self.angle, self.speed, math.pi, 0.002)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag


    def bounce(self):
        if self.x > len(img) - self.size:
            self.x = 2 * (len(img) - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > len(img[0]) - self.size:
            self.y = 2 * (len(img[0]) - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity


player = Particle(500, 500, 20)


class Line():
    def __init__(self, xstart, ystart, xend, yend):
        self.xstart = xstart
        self.ystart = ystart
        self.xend = xend
        self.yend = yend
        self.thickness = 5
        self.color = (0, 0, 0)
        start = []
        end = []
    def draw(self):
        pygame.draw.line(screen, self.color, (int(self.xstart), int(self.ystart)), (int(self.xend), int(self.yend)), self.thickness)





while True:

    # ret, frame = camera.read()
    frame = getImg()

    screen.fill([0, 0, 0])
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0, 0))

    lines = []

    player = Particle(100, 100, 20)
    player.display()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event == ord('h'):
                print("h")
