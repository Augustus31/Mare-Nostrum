import pygame
import os
import numpy as np
import random
import math
import copy
import ctypes
import traceback

##os.environ['SDL_VIDEODRIVER'] = 'directx'

# Query DPI Awareness (Windows 10 and 8)
awareness = ctypes.c_int()
errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
print(awareness.value)

# Set DPI Awareness  (Windows 10 and 8)
errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
# the argument is the awareness level, which can be 0, 1 or 2:
# for 1-to-1 pixel control I seem to need it to be non-zero (I'm using level 2)

# Set DPI Awareness  (Windows 7 and Vista)
success = ctypes.windll.user32.SetProcessDPIAware()
# behaviour on later OSes is undefined, although when I run it on my Windows 10

pygame.init()
pygame.mixer.init()
dwidth = 1280
dheight = 720
gameDisplay = pygame.display.set_mode((dwidth, dheight), pygame.FULLSCREEN)
pygame.display.set_caption('Mare Nostrum')
clock = pygame.time.Clock()
bgColor = (64, 64, 64)
black = (0,0,0)
white = (255, 255, 255)
level = 1

landtile = pygame.image.load('files/land tile.png')
seatile = pygame.image.load('files/sea tile.jpg')
ob = pygame.transform.smoothscale(pygame.image.load('files/orangeboat.png'), (35,20))
rb = pygame.transform.smoothscale(pygame.image.load('files/redboat.png'), (35,20))
yb = pygame.transform.smoothscale(pygame.image.load('files/yellowboat.png'), (35,20))
pb = pygame.transform.smoothscale(pygame.image.load('files/purpleboat.png'), (35,20))
x1 = pygame.transform.smoothscale(pygame.image.load('files/redx.png'), (30,30))
x2 = pygame.transform.smoothscale(pygame.image.load('files/redx2.png'), (30,30))
loading = pygame.image.load('files/loading.jpg')
wsuccess = pygame.transform.smoothscale(pygame.image.load('files/success.png'),(1280,720))
esuccess = pygame.transform.smoothscale(pygame.image.load('files/success2.png'),(1280,720))
failure = pygame.transform.smoothscale(pygame.image.load('files/failure.png'),(1280,720))
title = pygame.transform.smoothscale(pygame.image.load('files/title.png'),(1280,720))
ititle = pygame.transform.smoothscale(pygame.image.load('files/title2.png'),(1280,720))
cpanel = pygame.image.load('files/cpanel.png')

arrowsi = pygame.transform.smoothscale(pygame.image.load('files/arrows.png'),(65,73))
arrows_t = pygame.transform.smoothscale(pygame.image.load('files/arrows_t.png'),(65,73))
controli = pygame.transform.smoothscale(pygame.image.load('files/Fist.png'),(52,77))
control_t = pygame.transform.smoothscale(pygame.image.load('files/Fist_t.png'),(52,77))

rules1 = pygame.transform.smoothscale(pygame.image.load('files/rules1.png'),(1280,720))
rules2 = pygame.transform.smoothscale(pygame.image.load('files/rules2.png'),(1280,720))

track1 = pygame.mixer.Sound('files/sea.wav')
track1.set_volume(0.5)
track2 = pygame.mixer.Sound('files/aggression.wav')
track2.set_volume(0.5)
track3 = pygame.mixer.Sound('files/chase.wav')
track3.set_volume(0.5)

playermovesound = pygame.mixer.Sound('files/playermovesound.wav')
aimovesound = pygame.mixer.Sound('files/aimovesound.wav')
firesound = pygame.mixer.Sound('files/firesound.wav')
nextturnsound = pygame.mixer.Sound('files/nextturnsound.wav')
powerupsound = pygame.mixer.Sound('files/powerupsound.wav')
successsound = pygame.mixer.Sound('files/successsound.wav')
failuresound = pygame.mixer.Sound('files/failuresound.wav')
playermovesound.set_volume(0.5)
aimovesound.set_volume(0.5)
firesound.set_volume(0.5)
nextturnsound.set_volume(50)
powerupsound.set_volume(0.35)
successsound.set_volume(0.75)
failuresound.set_volume(10)

musicArray = [track1,track2,track3]

boardArray1 = np.ndarray((18,24), int)
boardArray2 = np.ndarray((18,24), int)

player = [12,1]

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(text, n, m, size, font, color):
    font = pygame.font.SysFont(font, size)
    ##largeText = pygame.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect = text_objects(text, font, color)
    TextRect.midleft = (int(n)),(int(m))
    gameDisplay.blit(TextSurf, TextRect)

def message_display_center(text, n, m, size, font, color):
    font = pygame.font.SysFont(font, size)
    ##largeText = pygame.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect = text_objects(text, font, color)
    TextRect.center = (int(n)),(int(m))
    gameDisplay.blit(TextSurf, TextRect)

def place(a,x,y):
    gameDisplay.blit(a, (x,y))

def centralPlace(a,cx,cy):
    gameDisplay.blit(a, (cx-(a.get_width()/2), cy-(a.get_height()/2)))

def gridToCoords(row, col):
    y = 20 + 40*row
    x = 20 + 40*col
    return (x,y)

def coordsToGrid(x, y):
    row = round((y - 20)/40)
    col = round((x - 20)/40)
    return (row, col)

def levelSet():
    global boardArray1, boardArray2, level
    for i in range(18):
        for j in range(24):
            s = random.random()
            if(s < 0.1 and i > 1 and i < 17 and j > 0 and j < 23):
                boardArray1[i][j] = 2
                boardArray1[i][j+1] = 1
                boardArray1[i][j-1] = 1
                boardArray1[i+1][j+1] = 1
                boardArray1[i+1][j] = 1
                boardArray1[i+1][j-1] = 1
                boardArray1[i-1][j+1] = 1
                boardArray1[i-1][j] = 1
                boardArray1[i-1][j-1] = 1
            else:
                boardArray1[i][j] = 1
    # checkArray = np.ndarray((18,24), int)
    # for i in range(18):
    #     for j in range(24):
    #         checkArray[i][j] = 0
    #
    # visitedCoords = (12, 1)
    # checkArray[12][1] = 1
    # for i in range(100000):
    #     possibleCoords = []
    #     for j in range(-1, 2, 1):
    #         if visitedCoords[0] + j < 18 and visitedCoords[0] + j >= 0:
    #             if boardArray1[visitedCoords[0] + j][visitedCoords[1]] == 1:
    #                 possibleCoords.append((visitedCoords[0] + j,visitedCoords[1]))
    #
    #     for k in range(-1, 2, 1):
    #         if visitedCoords[1] + k < 24 and visitedCoords[1] + k >= 0:
    #             if boardArray1[visitedCoords[0]][visitedCoords[1] + k] == 1:
    #                 possibleCoords.append((visitedCoords[0],visitedCoords[1] + k))
    #
    #     c = int((random.random()*len(possibleCoords)))
    #     visitedCoords = possibleCoords[c]
    #     checkArray[visitedCoords[0]][visitedCoords[1]] = 1
    # for i in range(18):
    #     for j in range(24):
    #         if boardArray1[i][j] == 1 and checkArray[i][j] == 0:
    #             levelSet()

    for i in range(18):
        for j in range(24):
            boardArray2[i][j] = 0

    numSpawned = 0
    for i in range(18):
        for j in range(0,24):
            if not (i==12 and j==1):
                if boardArray1[i][j] == 1:
                    s = random.random()*100
                    if numSpawned < 4 + 2.2*level and i >= 16:
                        if s < 5*((1.2)**level):
                            boardArray2[i][j] = 1
                            numSpawned = numSpawned + 1
                    elif s < 1.65*((1.2)**(level)):
                        boardArray2[i][j] = 1
                        numSpawned = numSpawned + 1
    boardArray2[12][1] = 4
    boardArray1[12][1] = 1

# def AIMove():
#     for i in range(18):
#         for j in range(32):
#             ardval = []
#             if boardArray2[i][j] == 1 or boardArray2[i][j] == 2 or boardArray2[i][j] == 3:
#                 if j+1 < 32 and boardArray1[i][j+1] == 1 and boardArray2[i][j+1] == 0:
#                     pessoa = 0
#                     if abs(player[1] - (j+1)) < abs(player[1] - j):
#                         pessoa = pessoa + (32 - (player[1]-(j+1)))
#                     for k in range(18):
#                         for l in range(32):
#                             if boardArray2[k][l] == 1 or boardArray2[k][l] == 2 or boardArray2[k][l] == 3:
#                                 if i == k and abs(l - (j+1)) == 1:
#                                     pessoa += 10
#                                 elif l == j+1 and abs(k - i) == 1:
#                                     pessoa += 10
#                     ardval.append(pessoa)
#                 else:
#                     ardval.append(-1)
#                 if j-1 >= 0 and boardArray1[i][j-1] == 1 and boardArray2[i][j-1] == 0:
#                     pessoa = 0
#                     if abs(player[1] - (j-1)) < abs(player[1] - j):
#                         pessoa = pessoa + (32 - (player[1]-(j-1)))
#                     for k in range(18):
#                         for l in range(32):
#                             if boardArray2[k][l] == 1 or boardArray2[k][l] == 2 or boardArray2[k][l] == 3:
#                                 if i == k and abs(l - (j-1)) == 1:
#                                     pessoa += 10
#                                 elif l == j-1 and abs(k - i) == 1:
#                                     pessoa += 10
#                     ardval.append(pessoa)
#                 else:
#                     ardval.append(-1)
#
#
#                 if i+1 < 18 and boardArray1[i+1][j] == 1 and boardArray2[i+1][j] == 0:
#                     pessoa = 0
#                     if abs(player[0] - (i+1)) < abs(player[0] - i):
#                         pessoa = pessoa + (32 - (player[0]-(i+1)))
#                     for k in range(18):
#                         for l in range(32):
#                             if boardArray2[k][l] == 1 or boardArray2[k][l] == 2 or boardArray2[k][l] == 3:
#                                 if j == l and abs(k - (i+1)) == 1:
#                                     pessoa += 10
#                                 elif k == i+1 and abs(l - j) == 1:
#                                     pessoa += 10
#                     ardval.append(pessoa)
#                 else:
#                     ardval.append(-1)
#
#
#                 if i-1 < 18 and boardArray1[i-1][j] == 1 and boardArray2[i-1][j] == 0:
#                     pessoa = 0
#                     if abs(player[0] - (i-1)) < abs(player[0] - i):
#                         pessoa = pessoa + (32 - (player[0]-(i-1)))
#                     for k in range(18):
#                         for l in range(32):
#                             if boardArray2[k][l] == 1 or boardArray2[k][l] == 2 or boardArray2[k][l] == 3:
#                                 if j == l and abs(k - (i-1)) == 1:
#                                     pessoa += 10
#                                 elif k == i-1 and abs(l - j) == 1:
#                                     pessoa += 10
#                     ardval.append(pessoa)
#                 else:
#                     ardval.append(-1)
#
#                 if ardval.index(max(ardval)) == 0:
#                     s = random.random()
#                     if boardArray2[i][j] == 1:
#                         if s < 0.5:
#                             boardArray2[i][j+1] = copy.deepcopy(boardArray2[i][j])
#                             boardArray2[i][j] = 0
#                         else:
#                             prereq = False
#                             while not prereq:
#                                 s2 = int(random.random()*len(ardval))
#                                 if ardval[s2] != -1:
#                                     prereq = True
#                                     if s2 == 0:
#                                         boardArray2[i][j+1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 1:
#                                         boardArray2[i][j-1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 2:
#                                         boardArray2[i+1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 3:
#                                         boardArray2[i-1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#
#                     if boardArray2[i][j] == 2:
#                         if s < 0.7:
#                             boardArray2[i][j+1] = copy.deepcopy(boardArray2[i][j])
#                             boardArray2[i][j] = 0
#                         else:
#                             prereq = False
#                             while not prereq:
#                                 s2 = int(random.random()*len(ardval))
#                                 if ardval[s2] != -1:
#                                     prereq = True
#                                     if s2 == 0:
#                                         boardArray2[i][j+1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 1:
#                                         boardArray2[i][j-1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 2:
#                                         boardArray2[i+1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 3:
#                                         boardArray2[i-1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                     if boardArray2[i][j] == 3:
#                         if s < 0.9:
#                             boardArray2[i][j+1] = copy.deepcopy(boardArray2[i][j])
#                             boardArray2[i][j] = 0
#                         else:
#                             prereq = False
#                             while not prereq:
#                                 s2 = int(random.random()*len(ardval))
#                                 if ardval[s2] != -1:
#                                     prereq = True
#                                     if s2 == 0:
#                                         boardArray2[i][j+1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 1:
#                                         boardArray2[i][j-1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 2:
#                                         boardArray2[i+1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 3:
#                                         boardArray2[i-1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#
#                 if ardval.index(max(ardval)) == 1:
#                     s = random.random()
#                     if boardArray2[i][j] == 1:
#                         if s < 0.5:
#                             boardArray2[i][j-1] = copy.deepcopy(boardArray2[i][j])
#                             boardArray2[i][j] = 0
#                         else:
#                             prereq = False
#                             while not prereq:
#                                 s2 = int(random.random()*len(ardval))
#                                 if ardval[s2] != -1:
#                                     prereq = True
#                                     if s2 == 0:
#                                         boardArray2[i][j+1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 1:
#                                         boardArray2[i][j-1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 2:
#                                         boardArray2[i+1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 3:
#                                         boardArray2[i-1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#
#                     if boardArray2[i][j] == 2:
#                         if s < 0.7:
#                             boardArray2[i][j-1] = copy.deepcopy(boardArray2[i][j])
#                             boardArray2[i][j] = 0
#                         else:
#                             prereq = False
#                             while not prereq:
#                                 s2 = int(random.random()*len(ardval))
#                                 if ardval[s2] != -1:
#                                     prereq = True
#                                     if s2 == 0:
#                                         boardArray2[i][j+1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 1:
#                                         boardArray2[i][j-1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 2:
#                                         boardArray2[i+1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 3:
#                                         boardArray2[i-1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                     if boardArray2[i][j] == 3:
#                         if s < 0.9:
#                             boardArray2[i][j-1] = copy.deepcopy(boardArray2[i][j])
#                             boardArray2[i][j] = 0
#                         else:
#                             prereq = False
#                             while not prereq:
#                                 s2 = int(random.random()*len(ardval))
#                                 if ardval[s2] != -1:
#                                     prereq = True
#                                     if s2 == 0:
#                                         boardArray2[i][j+1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 1:
#                                         boardArray2[i][j-1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 2:
#                                         boardArray2[i+1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 3:
#                                         boardArray2[i-1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#
#                 if ardval.index(max(ardval)) == 2:
#                     s = random.random()
#                     if boardArray2[i][j] == 1:
#                         if s < 0.5:
#                             boardArray2[i+1][j] = copy.deepcopy(boardArray2[i][j])
#                             boardArray2[i][j] = 0
#                         else:
#                             prereq = False
#                             while not prereq:
#                                 s2 = int(random.random()*len(ardval))
#                                 if ardval[s2] != -1:
#                                     prereq = True
#                                     if s2 == 0:
#                                         boardArray2[i][j+1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 1:
#                                         boardArray2[i][j-1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 2:
#                                         boardArray2[i+1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 3:
#                                         boardArray2[i-1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#
#                     if boardArray2[i][j] == 2:
#                         if s < 0.7:
#                             boardArray2[i+1][j] = copy.deepcopy(boardArray2[i][j])
#                             boardArray2[i][j] = 0
#                         else:
#                             prereq = False
#                             while not prereq:
#                                 s2 = int(random.random()*len(ardval))
#                                 if ardval[s2] != -1:
#                                     prereq = True
#                                     if s2 == 0:
#                                         boardArray2[i][j+1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 1:
#                                         boardArray2[i][j-1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 2:
#                                         boardArray2[i+1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 3:
#                                         boardArray2[i-1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                     if boardArray2[i][j] == 3:
#                         if s < 0.9:
#                             boardArray2[i+1][j] = copy.deepcopy(boardArray2[i][j])
#                             boardArray2[i][j] = 0
#                         else:
#                             prereq = False
#                             while not prereq:
#                                 s2 = int(random.random()*len(ardval))
#                                 if ardval[s2] != -1:
#                                     prereq = True
#                                     if s2 == 0:
#                                         boardArray2[i][j+1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 1:
#                                         boardArray2[i][j-1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 2:
#                                         boardArray2[i+1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 3:
#                                         boardArray2[i-1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                 if ardval.index(max(ardval)) == 3:
#                     s = random.random()
#                     if boardArray2[i][j] == 1:
#                         if s < 0.5:
#                             boardArray2[i-1][j] = copy.deepcopy(boardArray2[i][j])
#                             boardArray2[i][j] = 0
#                         else:
#                             prereq = False
#                             while not prereq:
#                                 s2 = int(random.random()*len(ardval))
#                                 if ardval[s2] != -1:
#                                     prereq = True
#                                     if s2 == 0:
#                                         boardArray2[i][j+1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 1:
#                                         boardArray2[i][j-1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 2:
#                                         boardArray2[i+1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 3:
#                                         boardArray2[i-1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#
#                     if boardArray2[i][j] == 2:
#                         if s < 0.7:
#                             boardArray2[i-1][j] = copy.deepcopy(boardArray2[i][j])
#                             boardArray2[i][j] = 0
#                         else:
#                             prereq = False
#                             while not prereq:
#                                 s2 = int(random.random()*len(ardval))
#                                 if ardval[s2] != -1:
#                                     prereq = True
#                                     if s2 == 0:
#                                         boardArray2[i][j+1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 1:
#                                         boardArray2[i][j-1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 2:
#                                         boardArray2[i+1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 3:
#                                         boardArray2[i-1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                     if boardArray2[i][j] == 3:
#                         if s < 0.9:
#                             boardArray2[i-1][j] = copy.deepcopy(boardArray2[i][j])
#                             boardArray2[i][j] = 0
#                         else:
#                             prereq = False
#                             while not prereq:
#                                 s2 = int(random.random()*len(ardval))
#                                 if ardval[s2] != -1:
#                                     prereq = True
#                                     if s2 == 0:
#                                         boardArray2[i][j+1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 1:
#                                         boardArray2[i][j-1] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 2:
#                                         boardArray2[i+1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
#                                     elif s2 == 3:
#                                         boardArray2[i-1][j] = copy.deepcopy(boardArray2[i][j])
#                                         boardArray2[i][j] = 0
prow = 12
pcol = 1
moves = 6
hmoves = 3
shots = 1
firemode = False
fireArray = [0,0,0,0,0]

def randomMove():
    try:
        global prow,pcol,moves,hmoves,shots,fireArray,firemode,boardArray1,boardArray2
        r1 = random.random()
        nearby = False
        nloc = (-1,-1)
        for i in range(-3,4,1):
            if(pcol + i >= 0 and pcol + i <= 23 and boardArray2[prow][pcol+i] == 1):
                nearby = True
                nloc = (prow,pcol+i)
            elif (prow + i >= 0 and prow + i <= 17 and boardArray2[prow+i][pcol] == 1):
                nearby = True
                nloc = (prow+i,pcol)
        if nearby:
            if r1 <= 0.6 and shots > 0:
                r2 = random.random()
                if r2 < 0.8:
                    shots = shots - 1
                    moves = moves - 1
                    fireArray = [1,gridToCoords(nloc[0],nloc[1])[0],gridToCoords(nloc[0],nloc[1])[1],nloc[0],nloc[1]]
                    boardArray2[nloc[0],nloc[1]] = 0
                    if not pygame.mixer.Channel(4).get_busy():
                        pygame.mixer.Channel(4).play(firesound)
                else:
                    r9 = random.random()
                    if r9 < 0.25 and prow+1 <= 17:
                        shots = shots -1
                        moves = moves -1
                        fireArray = [1,gridToCoords(prow+1,pcol)[0],gridToCoords(prow+1,pcol)[1],prow+1,pcol]
                        boardArray2[prow+1,pcol] = 0
                        if not pygame.mixer.Channel(4).get_busy():
                            pygame.mixer.Channel(4).play(firesound)
                    elif r9 < 0.5 and prow-1 >= 0:
                        shots = shots -1
                        moves = moves -1
                        fireArray = [1,gridToCoords(prow-1,pcol)[0],gridToCoords(prow-1,pcol)[1],prow-1,pcol]
                        boardArray2[prow-1,pcol] = 0
                        if not pygame.mixer.Channel(4).get_busy():
                            pygame.mixer.Channel(4).play(firesound)
                    elif r9 < 0.75 and pcol+1 <= 23:
                        shots = shots -1
                        moves = moves -1
                        fireArray = [1,gridToCoords(prow,pcol+1)[0],gridToCoords(prow,pcol+1)[1],prow,pcol+1]
                        boardArray2[prow,pcol+1] = 0
                        if not pygame.mixer.Channel(4).get_busy():
                            pygame.mixer.Channel(4).play(firesound)
                    elif pcol-1 >= 0:
                        shots = shots -1
                        moves = moves -1
                        fireArray = [1,gridToCoords(prow,pcol-1)[0],gridToCoords(prow,pcol-1)[1],prow,pcol-1]
                        boardArray2[prow,pcol-1] = 0
                        if not pygame.mixer.Channel(4).get_busy():
                            pygame.mixer.Channel(4).play(firesound)

                    # # if prow == nloc[0]:
                    # #     r3 = round(random.random()*6-3)
                    # #     if r3 == 0:
                    # #         r3 = 3
                    # #     if (nloc[0]+r3) > 17:
                    # #         diff = 17 - (nloc[0]+r3)
                    # #         r3 = r3 + diff
                    # #     if (nloc[0]+r3) < 0:
                    # #         diff = 0 - (nloc[0]+r3)
                    # #         r3 = r3 + diff
                    # #     shots = shots - 1
                    # #     moves = moves - 1
                    # #     fireArray = [1,gridToCoords(nloc[0]+r3,nloc[1])[0],gridToCoords(nloc[0]+r3,nloc[1])[1],nloc[0]+r3,nloc[1]]
                    # #     boardArray2[nloc[0]+r3,nloc[1]] = 0
                    # else:
                    #     r3 = round(random.random()*6-3)
                    #     if r3 == 0:
                    #         r3 = 3
                    #     if (nloc[1]+r3) > 23:
                    #         diff = 17 - (nloc[1]+r3)
                    #         r3 = r3 + diff
                    #     if (nloc[1]+r3) < 0:
                    #         diff = 0 - (nloc[1]+r3)
                    #         r3 = r3 + diff
                    #     shots = shots - 1
                    #     moves = moves - 1
                    #     fireArray = [1,gridToCoords(nloc[0],nloc[1]+r3)[0],gridToCoords(nloc[0],nloc[1]+r3)[1],nloc[0],nloc[1]+r3]
                    #     boardArray2[nloc[0],nloc[1]+r3] = 0
            else:
                r4 = random.random()
                if r4 < 0.25 and pcol - 1 >= 0 and boardArray1[prow][pcol-1] == 1 and boardArray2[prow][pcol-1] == 0:
                    boardArray2[prow][pcol] = 0
                    pcol = pcol - 1
                    moves = moves - 1
                    if not pygame.mixer.Channel(2).get_busy():
                        pygame.mixer.Channel(2).play(playermovesound)
                elif r4 < 0.5 and pcol + 1 <= 23 and boardArray1[prow][pcol+1] == 1 and boardArray2[prow][pcol+1] == 0:
                    boardArray2[prow][pcol] = 0
                    pcol = pcol + 1
                    moves = moves - 1
                    if not pygame.mixer.Channel(2).get_busy():
                        pygame.mixer.Channel(2).play(playermovesound)
                elif r4 < 0.75 and prow + 1 <= 17 and boardArray1[prow+1][pcol] == 1 and boardArray2[prow+1][pcol] == 0:
                    boardArray2[prow][pcol] = 0
                    prow = prow + 1
                    moves = moves - 1
                    if not pygame.mixer.Channel(2).get_busy():
                        pygame.mixer.Channel(2).play(playermovesound)
                elif prow - 1 >= 0 and boardArray1[prow-1][pcol] == 1 and boardArray2[prow-1][pcol] == 0:
                    boardArray2[prow][pcol] = 0
                    prow = prow - 1
                    moves = moves - 1
                    if not pygame.mixer.Channel(2).get_busy():
                        pygame.mixer.Channel(2).play(playermovesound)
        else:
            r5 = random.random()
            if r5 < 0.11 and shots > 0:
                r9 = random.random()
                if r9 < 0.25 and prow+1 <= 17:
                    shots = shots -1
                    moves = moves -1
                    fireArray = [1,gridToCoords(prow+1,pcol)[0],gridToCoords(prow+1,pcol)[1],prow+1,pcol]
                    boardArray2[prow+1,pcol] = 0
                    if not pygame.mixer.Channel(4).get_busy():
                        pygame.mixer.Channel(4).play(firesound)
                elif r9 < 0.5 and prow-1 >= 0:
                    shots = shots -1
                    moves = moves -1
                    fireArray = [1,gridToCoords(prow-1,pcol)[0],gridToCoords(prow-1,pcol)[1],prow-1,pcol]
                    boardArray2[prow-1,pcol] = 0
                    if not pygame.mixer.Channel(4).get_busy():
                        pygame.mixer.Channel(4).play(firesound)
                elif r9 < 0.75 and pcol+1 <= 23:
                    shots = shots -1
                    moves = moves -1
                    fireArray = [1,gridToCoords(prow,pcol+1)[0],gridToCoords(prow,pcol+1)[1],prow,pcol+1]
                    boardArray2[prow,pcol+1] = 0
                    if not pygame.mixer.Channel(4).get_busy():
                        pygame.mixer.Channel(4).play(firesound)
                elif pcol-1 >= 0:
                    shots = shots -1
                    moves = moves -1
                    fireArray = [1,gridToCoords(prow,pcol-1)[0],gridToCoords(prow,pcol-1)[1],prow,pcol-1]
                    boardArray2[prow,pcol-1] = 0
                    if not pygame.mixer.Channel(4).get_busy():
                        pygame.mixer.Channel(4).play(firesound)
            elif r5 < 0.22 and shots > 0:
                r9 = random.random()
                if r9 < 0.25 and prow+1 <= 17:
                    shots = shots -1
                    moves = moves -1
                    fireArray = [1,gridToCoords(prow+1,pcol)[0],gridToCoords(prow+1,pcol)[1],prow+1,pcol]
                    boardArray2[prow+1,pcol] = 0
                    if not pygame.mixer.Channel(4).get_busy():
                        pygame.mixer.Channel(4).play(firesound)
                elif r9 < 0.5 and prow-1 >= 0:
                    shots = shots -1
                    moves = moves -1
                    fireArray = [1,gridToCoords(prow-1,pcol)[0],gridToCoords(prow-1,pcol)[1],prow-1,pcol]
                    boardArray2[prow-1,pcol] = 0
                    if not pygame.mixer.Channel(4).get_busy():
                        pygame.mixer.Channel(4).play(firesound)
                elif r9 < 0.75 and pcol+1 <= 23:
                    shots = shots -1
                    moves = moves -1
                    fireArray = [1,gridToCoords(prow,pcol+1)[0],gridToCoords(prow,pcol+1)[1],prow,pcol+1]
                    boardArray2[prow,pcol+1] = 0
                    if not pygame.mixer.Channel(4).get_busy():
                        pygame.mixer.Channel(4).play(firesound)
                elif pcol-1 >= 0:
                    shots = shots -1
                    moves = moves -1
                    fireArray = [1,gridToCoords(prow,pcol-1)[0],gridToCoords(prow,pcol-1)[1],prow,pcol-1]
                    boardArray2[prow,pcol-1] = 0
                    if not pygame.mixer.Channel(4).get_busy():
                        pygame.mixer.Channel(4).play(firesound)
            else:
                r4 = random.random()
                if r4 < 0.25 and pcol - 1 >= 0 and boardArray1[prow][pcol-1] == 1 and boardArray2[prow][pcol-1] == 0:
                    boardArray2[prow][pcol] = 0
                    pcol = pcol - 1
                    moves = moves - 1
                    if not pygame.mixer.Channel(2).get_busy():
                        pygame.mixer.Channel(2).play(playermovesound)
                elif r4 < 0.5 and pcol + 1 <= 23 and boardArray1[prow][pcol+1] == 1 and boardArray2[prow][pcol+1] == 0:
                    boardArray2[prow][pcol] = 0
                    pcol = pcol + 1
                    moves = moves - 1
                    if not pygame.mixer.Channel(2).get_busy():
                        pygame.mixer.Channel(2).play(playermovesound)
                elif r4 < 0.75 and prow + 1 <= 17 and boardArray1[prow+1][pcol] == 1 and boardArray2[prow+1][pcol] == 0:
                    boardArray2[prow][pcol] = 0
                    prow = prow + 1
                    moves = moves - 1
                    if not pygame.mixer.Channel(2).get_busy():
                        pygame.mixer.Channel(2).play(playermovesound)
                elif prow - 1 >= 0 and boardArray1[prow-1][pcol] == 1 and boardArray2[prow-1][pcol] == 0:
                    boardArray2[prow][pcol] = 0
                    prow = prow - 1
                    moves = moves - 1
                    if not pygame.mixer.Channel(2).get_busy():
                        pygame.mixer.Channel(2).play(playermovesound)
    except Exception as e:
        traceback.print_exc()
        randomMove()

def AIMove():
    global prow,pcol,moves,hmoves,shots,fireArray,firemode,boardArray1,boardArray2
    ailist = []
    for i in range(18):
        for j in range(24):
            if boardArray2[i][j] == 1:
                ailist.append((i,j))

    for (i,j) in ailist:
        try:
            r1 = random.random()*100
            dm = [0,0]
            if i < prow:
                dm[0] = 1
            elif i > prow:
                dm[0] = -1
            if j < pcol:
                dm[1] = 1
            elif j > pcol:
                dm[1]= -1
            if i + dm[0] <= 17 and i + dm[0] >= 0 and boardArray2[i+dm[0]][j] != 1 and boardArray1[i+dm[0]][j] == 1 and r1 < ((66 + level*2.5)/2) and dm[0] != 0:
                boardArray2[i+dm[0]][j] = 1
                boardArray2[i][j] = 0
                if not pygame.mixer.Channel(3).get_busy():
                    pygame.mixer.Channel(3).play(aimovesound)
            elif j + dm[1] <= 23 and j + dm[1] >= 0 and boardArray2[i][j+dm[1]] != 1 and boardArray1[i][j+dm[1]] == 1 and r1 < (66 + level*2.5) and dm[1] != 0:
                boardArray2[i][j+dm[1]] = 1
                boardArray2[i][j] = 0
                if not pygame.mixer.Channel(3).get_busy():
                    pygame.mixer.Channel(3).play(aimovesound)
            else:
                r2 = random.random()
                if r2 < 0.4 + 0.02*level:
                    pass
                elif i - dm[0] <= 17 and i - dm[0] >= 0 and boardArray2[i-dm[0]][j] != 1 and boardArray1[i-dm[0]][j] == 1 and r2 < 0.7 + 0.01*level:
                    boardArray2[i-dm[0]][j] = 1
                    boardArray2[i][j] = 0
                    if not pygame.mixer.Channel(3).get_busy():
                        pygame.mixer.Channel(3).play(aimovesound)
                elif j - dm[1] <= 23 and j - dm[1] >= 0 and boardArray2[i][j-dm[1]] != 1 and boardArray1[i][j-dm[1]] == 1:
                    boardArray2[i][j-dm[1]] = 1
                    boardArray2[i][j] = 0
                    if not pygame.mixer.Channel(3).get_busy():
                        pygame.mixer.Channel(3).play(aimovesound)
        except Exception as e:
            traceback.print_exc()

def ititleLoop():
    global level
    end = False
    while not end:
        if not pygame.mixer.Channel(1).get_busy():
            pygame.mixer.Channel(1).play(track1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                end = True
        gameDisplay.fill((113,113,113))
        centralPlace(ititle, dwidth/2,dheight/2)
        pygame.display.update()
        n = clock.tick()

def rulesLoop1():
    global level
    end = False
    while not end:
        # if not pygame.mixer.Channel(1).get_busy():
        #     pygame.mixer.Channel(1).play(musicArray[int(random.random()*len(musicArray))])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                rulesLoop2()
                end = True
        gameDisplay.fill((113,113,113))
        centralPlace(rules1, dwidth/2,dheight/2)
        pygame.display.update()
        n = clock.tick()

def rulesLoop2():
    global level
    end = False
    while not end:
        # if not pygame.mixer.Channel(1).get_busy():
        #     pygame.mixer.Channel(1).play(musicArray[int(random.random()*len(musicArray))])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                gameLoop()
                end = True
        gameDisplay.fill((113,113,113))
        centralPlace(rules2, dwidth/2,dheight/2)
        pygame.display.update()
        n = clock.tick()

def titleLoop():
    global level
    end = False
    while not end:
        # if not pygame.mixer.Channel(1).get_busy():
        #     pygame.mixer.Channel(1).play(musicArray[int(random.random()*len(musicArray))])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if x > 364 and x < 407 and y > 363 and y < 406:
                    end = True
                    level = 1
                    rulesLoop1()
                elif x > 913 and x < 956 and y > 583 and y < 626:
                    end = True
                    level = 4
                    rulesLoop1()
        gameDisplay.fill((113,113,113))
        centralPlace(title, dwidth/2,dheight/2)
        pygame.display.update()
        n = clock.tick()


def gameLoop():
    global prow,pcol,moves,hmoves,shots,firemode,fireArray,level
    end = False
    # centralPlace(loading, dwidth/2, dheight/2)
    pygame.display.update()
    levelSet()
    prow = 12
    pcol = 1
    moves = 6
    hmoves = 3
    if level <= 3:
        shots = 1
    else:
        shots = 1
    firemode = False
    fireArray = [0,0,0,0,0]
    aimm = False
    startTime = 0
    aimoves = 0
    control = True
    arrows = True
    arrowsactive = False
    arrowsarray = [0,0,0]

    while not end:
        if not pygame.mixer.Channel(1).get_busy():
            if level <= 3:
                pygame.mixer.Channel(1).play(musicArray[0])
            else:
                pygame.mixer.Channel(1).play(musicArray[round(random.random()+1)])
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and moves == 0:
                    moves = 6
                    hmoves = 3
                    if level <= 3:
                        shots = 1
                    else:
                        shots = 1
                    fireArray = [0,0,0,0,0]
                    startTime = pygame.time.get_ticks()
                    aimoves = 0
                    aimm = True
                    if not pygame.mixer.Channel(8).get_busy():
                        pygame.mixer.Channel(8).play(nextturnsound)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_a and moves > 0 and hmoves > 0 and boardArray1[prow][pcol-1]  == 1 and (pcol - 1 >= 0):
                    boardArray2[prow][pcol] = 0
                    pcol = pcol - 1
                    moves = moves - 1
                    hmoves = hmoves - 1
                    if not pygame.mixer.Channel(2).get_busy():
                        pygame.mixer.Channel(2).play(playermovesound)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d and moves > 0 and hmoves > 0 and boardArray1[prow][pcol+1] == 1 and (pcol + 1 <= 23):
                    boardArray2[prow][pcol] = 0
                    pcol = pcol + 1
                    moves = moves - 1
                    hmoves = hmoves - 1
                    if not pygame.mixer.Channel(2).get_busy():
                        pygame.mixer.Channel(2).play(playermovesound)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s and moves > 0 and hmoves > 0 and boardArray1[prow+1][pcol] == 1 and (prow + 1 <= 17):
                    boardArray2[prow][pcol] = 0
                    prow = prow + 1
                    moves = moves - 1
                    hmoves = hmoves - 1
                    if not pygame.mixer.Channel(2).get_busy():
                        pygame.mixer.Channel(2).play(playermovesound)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_w and moves > 0 and hmoves > 0 and boardArray1[prow-1][pcol] == 1 and (prow - 1 >= 0):
                    boardArray2[prow][pcol] = 0
                    prow = prow - 1
                    moves = moves - 1
                    hmoves = hmoves - 1
                    if not pygame.mixer.Channel(2).get_busy():
                        pygame.mixer.Channel(2).play(playermovesound)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    if firemode == True:
                        firemode = False
                    else:
                        firemode = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_c and control:
                    control = False
                    hmoves = moves
                    if not pygame.mixer.Channel(5).get_busy():
                        pygame.mixer.Channel(5).play(powerupsound)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_x and arrows:
                    arrows = False
                    hmoves = hmoves + 1
                    shots = hmoves
                    if not pygame.mixer.Channel(5).get_busy():
                        pygame.mixer.Channel(5).play(powerupsound)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and firemode and moves > 0 and hmoves > 0 and shots > 0:
                    clickX = pygame.mouse.get_pos()[0]
                    clickY = pygame.mouse.get_pos()[1]
                    (a,b) = coordsToGrid(clickX,clickY)
                    (x,y) = gridToCoords(a,b)
                    if ((a == prow and abs(b-pcol) <= 3) or (b == pcol and abs(a-prow) <= 3)):
                        shots = shots - 1
                        moves = moves - 1
                        hmoves = hmoves - 1
                        fireArray = [1,x,y,a,b]
                        boardArray2[a,b] = 0
                        if not pygame.mixer.Channel(4).get_busy():
                            pygame.mixer.Channel(4).play(firesound)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_r and moves > 0:
                    randomMove()
        except:
            pass
        gameDisplay.fill(bgColor)
        fail = False
        if boardArray2[prow][pcol] == 1:
            fail = True
        else:
            boardArray2[prow][pcol] = 4
        for i in range(18):
            for j in range(24):
                if boardArray1[i][j] == 1:
                    centralPlace(seatile, gridToCoords(i,j)[0], gridToCoords(i,j)[1])
                else:
                    centralPlace(landtile, gridToCoords(i,j)[0], gridToCoords(i,j)[1])
        for i in range(18):
            for j in range(24):
                if boardArray2[i][j] == 1:
                    centralPlace(rb, gridToCoords(i,j)[0], gridToCoords(i,j)[1])
                if boardArray2[i][j] == 4:
                    centralPlace(pb, gridToCoords(i,j)[0], gridToCoords(i,j)[1])

        locations = ["Pillars of Hercules", "Balearic Islands", "Gulf of Gabes", "Ionian Sea", "Dardanelles", "Coast of Cilicia"]
        place(cpanel, 960,0)
        message_display(str(locations[level-1]), 990, 40, 30, "Trebuchet MS", (0,0,0))
        message_display("Level: " + str(level), 990, 80, 30, "Trebuchet MS", (0,0,0))
        message_display("-----------------------", 990, 130, 30, "Trebuchet MS", (0,0,0))
        message_display("Moves: " + str(moves), 990, 180, 20, "Georgia", (0,0,0))
        message_display("Player Moves: " + str(hmoves), 990, 210, 20, "Georgia", (0,0,0))
        message_display("Shots: " + str(shots), 990, 240, 20, "Georgia", (0,0,0))
        message_display("Note: You MUST use all ", 990, 270, 20, "Georgia", (80,0,0))
        message_display("your moves each turn.", 990, 300, 20, "Georgia", (80,0,0))
        message_display("-----------------------", 990, 350, 30, "Trebuchet MS", (0,0,0))
        message_display("W, A, S, D to move.", 990, 400, 20, "Georgia", (0,80,0))
        message_display("F to enter fire mode.", 990, 430, 20, "Georgia", (0,80,0))
        message_display("R for random move.", 990, 460, 20, "Georgia", (0,80,0))
        message_display("Space for next turn.", 990, 490, 20, "Georgia", (0,80,0))
        message_display("-----------------------", 990, 540, 30, "Trebuchet MS", (0,0,0))

        if control:
            centralPlace(controli, 1050, 625)
            message_display_center("Press C", 1050, 680, 20, "Georgia", (0,80,0))
        else:
            centralPlace(control_t, 1050, 625)
            message_display_center("Disabled", 1050, 680, 20, "Georgia", (80,0,0))
        if arrows:
            centralPlace(arrowsi, 1160, 630)
            message_display_center("Press X", 1160, 680, 20, "Georgia", (0,80,0))
        else:
            centralPlace(arrows_t, 1160, 630)
            message_display_center("Disabled", 1160, 680, 20, "Georgia", (80,0,0))



        numAI = 0
        for i in range(18):
            for j in range(24):
                if boardArray2[i][j] == 1:
                    numAI = numAI + 1

        if numAI == 0:
            pygame.time.delay(400)
            if level == 3 or level == 6:
                if not pygame.mixer.Channel(6).get_busy():
                    pygame.mixer.Channel(6).play(successsound)
                successLoop()
            else:
                level = level + 1
                if not pygame.mixer.Channel(6).get_busy():
                    pygame.mixer.Channel(6).play(successsound)
                gameLoop()
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]

        if firemode:
            (a,b) = coordsToGrid(mouseX,mouseY)
            (x,y) = gridToCoords(a,b)
            if (a == prow and abs(b-pcol) <= 3) or (b == pcol and abs(a-prow) <= 3):
                centralPlace(x2,x,y)
        if fireArray[0] == 1:
            centralPlace(x1,fireArray[1],fireArray[2])

        if aimm:
            if pygame.time.get_ticks() - startTime >= 200:
                AIMove()
                startTime = pygame.time.get_ticks()
                aimoves = aimoves + 1


        if level == 1:
            if aimoves == 3:
                aimm = False
        if level <= 5:
            if aimoves == 4:
                aimm = False
        elif level <= 6:
            if aimoves == 5:
                aimm = False

        if fail:
            centralPlace(rb,gridToCoords(prow,pcol)[0], gridToCoords(prow,pcol)[1])
            pygame.display.update()
            if not pygame.mixer.Channel(7).get_busy():
                pygame.mixer.Channel(7).play(failuresound)
            pygame.time.delay(400)
            failLoop()
        pygame.display.update()
        clock.tick(60)

def failLoop():
    # pygame.mixer.Channel(3).play(failureSound)
    centralPlace(failure, dwidth/2, dheight/2)
    pygame.display.update()
    end = False
    while not end:
        # if not pygame.mixer.Channel(1).get_busy():
        #     pygame.mixer.Channel(1).play(musicArray[int(random.random()*len(musicArray))])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                gameLoop()

def successLoop():
    global level
    ##pygame.mixer.Channel(2).play(successSound)
    if level == 3:
        centralPlace(wsuccess, dwidth/2, dheight/2)
    elif level == 6:
        centralPlace(esuccess, dwidth/2, dheight/2)
    pygame.display.update()
    end = False
    while not end:
        # if not pygame.mixer.Channel(1).get_busy():
        #     pygame.mixer.Channel(1).play(musicArray[int(random.random()*len(musicArray))])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                titleLoop()
                pass
ititleLoop()
titleLoop()
gameLoop()

##Credits

##https://www.pngwing.com/en/free-png-zwsej/download
##https://freemusicarchive.org/music/Sergey_Cheremisinov/Sea__Night/Sergey_Cheremisinov_-_Sea__Night_-_02_Crystal_Echoes/
##https://freemusicarchive.org/music/Dee_Yan-Key/facts-of-life/05--Dee_Yan-Key-The_Sea/
##https://freemusicarchive.org/music/serge-quadrado/action/chase-2/
##https://freemusicarchive.org/music/serge-quadrado/action/agression/

##https://freesound.org/people/JonnyRuss01/sounds/478197/
##https://freesound.org/people/gusgus26/sounds/415090/
##https://freesound.org/people/Twisted_Euphoria/sounds/205938/
##https://freesound.org/people/ammaro/sounds/573381/
##https://freesound.org/people/MATRIXXX_/sounds/523655/
##https://freesound.org/people/distillerystudio/sounds/327738/
