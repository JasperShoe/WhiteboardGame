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
width = 1280
height = 720

drag = 0.999
elasticity = 0.75
gravity = (math.pi, 0.005)
touching = False
w = 1280
h = 720

img = None

global xStart, yStart, xEnd, yEnd
xStart = []
yStart = []
xEnd = []
yEnd = []


def getImg():
    ret_val, img = camera.read()
    img = cv.flip(img, 1)
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
    if side2 > 0:
        semi = int((side1+side2+side3)/2)

        area = math.sqrt(abs((semi)*(semi-side1)*(semi-side2)*(semi-side3)))

        # print(px)
        print(side2)
        height = int((2*area)/side2)
        #height = 2
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
        (self.angle, self.speed) = addVectors(self.angle, self.speed, math.pi, 3)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag


    def bounce(self):
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
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
        self.color = (0, 0, 255)

    def draw(self):
        pygame.draw.line(screen, self.color, (int(self.xstart), int(self.ystart)), (int(self.xend), int(self.yend)), self.thickness)
        # cv.line(img, (int(self.xstart), int(self.ystart)), (int(self.xend), int(self.yend)), self.color, self.thickness)



while True:
    # ret, frame = camera.read()
    frame = cv.flip(getImg(), 1)



    # Filters
    img_analyze = frame.copy()
    img_analyze = cv.medianBlur(img_analyze, 3)
    img_analyze = cv.cvtColor(img_analyze, cv.COLOR_BGR2GRAY)

    # #Detection Box
    win_w = len(img_analyze[0])
    win_h = len(img_analyze)
    pad_x = 200
    pad_y = 100
    cv.rectangle(img_analyze, (0, 0), (10, win_h), (0, 0, 0), thickness=-1)
    cv.rectangle(img_analyze, (10, 0), (win_w - 500, pad_y), (0, 0, 0), thickness=-1)
    cv.rectangle(img_analyze, (win_w - 500, 0), (win_w, win_h), (0, 0, 0), thickness=-1)
    cv.rectangle(img_analyze, (10, win_h - pad_y), (win_w - 500, win_h), (0, 0, 0), thickness=-1)

    # img = cv.flip(img, 1)

    # Contour Detection
    ret, thresh = cv.threshold(img_analyze, 127, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # for i in range(len(xStart)):
    #     cv.line(img, (xStart[i],yStart[i]), (xEnd[i],yEnd[i]), (0, 255, 0), 5)

    # draw contour on the screen
    # Drawing Contours
    cv.drawContours(frame, contours, -1, (0, 255, 0), 3)
    #
    # cv.imshow("Whiteboard Game", img)
    # cv.moveWindow("Whiteboard Game", 0, 0)

    k = cv.waitKey(1)
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    if keys[K_d]:
        #print("hola")
        xStart = []
        yStart = []
        xEnd = []
        yEnd = []

        x = []
        y = []
        for i in range(0, len(contours)):
            for r in range(len(contours[i])):
                x.append(contours[i][r][0][0])
                y.append(contours[i][r][0][1])

            if not min(x) == 11 and not y[np.where(x == min(x))[0][0]] == 101 or not max(x) == 779 and not y[
                                                                                                               np.where(
                                                                                                                       x == max(
                                                                                                                           x))[
                                                                                                                   0][
                                                                                                                   0]] == 619:
                xStart.append(min(x))
                z = np.where(x == min(x))
                z = z[0][0]

                yStart.append(y[z])

                xEnd.append(max(x))
                z = np.where(x == max(x))

                z = z[0][0]

                yEnd.append(y[z])

                # draw contour on the screen
                cv.line(img, (x[0], y[0]), (x[len(x) - 1], y[len(y) - 1]), (0, 255, 0), 5)

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
    # for event in events:
    #     if event.type == pygame.KEYUP:
    #         if event.key == pygame.K_d:
    #             xStart = []
    #             yStart = []
    #             xEnd = []
    #             yEnd = []
    #
    #             x = []
    #             y = []
    #             for i in range(0, len(contours)):
    #                 for r in range(len(contours[i])):
    #                     x.append(contours[i][r][0][0])
    #                     y.append(contours[i][r][0][1])
    #                     print("no u")
    #
    #                 if not min(x) == 11 and not y[np.where(x == min(x))[0][0]] == 101 or not max(x) == 779 and not y[
    #                                                                                                                    np.where(
    #                                                                                                                            x == max(
    #                                                                                                                                x))[
    #                                                                                                                        0][
    #                                                                                                                        0]] == 619:
    #                     xStart.append(min(x))
    #                     z = np.where(x == min(x))
    #                     z = z[0][0]
    #
    #                     yStart.append(y[z])
    #
    #                     xEnd.append(max(x))
    #                     z = np.where(x == max(x))
    #
    #                     z = z[0][0]
    #
    #                     yEnd.append(y[z])
    #
    #                     # draw contour on the screen
    #                     cv.line(img, (x[0], y[0]), (x[len(x) - 1], y[len(y) - 1]), (0, 255, 0), 5)
    #
    #                 x = []
    #                 y = []
    #
    #             # print(xStart)
    #             # print(yStart)
    #             # print(len(xStart))
    #             # print(len(yStart))
    #             #
    #             #
    #             # #print("test")
    #             # print(xEnd)
    #             # print(yEnd)
    #             # print(len(xEnd))
    #             # print(len(yEnd))
    #             # print(len(contours))
    #             break
    if not k == -1:
        print(k)
    if k == 27:
        sys.exit(0)

    #begin pygame code
    screen.fill([0, 0, 0])
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0, 0))

    lines = []

    #for loop to import line goes here
    for j in range(len(xStart)):
        lines.append(Line(xStart[j], yStart[j], xEnd[j], yEnd[j]))
        # jjj = Line(50, 50, 100, 100)
        # lines.append(jjj)
    touchedLine = []
    for x in range(len(lines)):
        touchedLine.append(0)
    # print(len(xStart))

    #test = Line(50, 50, 100, 100)
    #lines.append(test)


    #player = Particle(100, 100, 20)
    selected_particle = None

    #runs the pygame code
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = player
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5 * math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.1



    player.move()
    player.bounce()
    player.display()
    #test.draw()

    # for i, Line in enumerate(lines):
    #     # if touchedLine[i] < 0:
    #     #     if collideLine(player, lines[i]) == True:
    #     #         touchedLine[i] = 10
    #     # touchedLine[i] -= 1
    #     lines[i].draw()

    for i in range(len(lines)):
        lines[i].draw()
        # collideLine(player, lines[i])


    # pygame.transform.flip(screen, True, False)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event == ord('h'):
                print("h")






    # pygame.display.flip()