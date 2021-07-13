# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 12:53:27 2021

@author: njoos
"""

import math
import pygame
from pygame.locals import *
import random
import sys
# import time

#    0
#  0 +---------+
#    |         |
#    |         |
#    |         |
#    |         |
#    |         |
#    +---------+ frame_w
#              f
#              r
#              a
#              m
#              e
#              _
#              h

# defines the window size
frame_w = 1000
frame_h = 500

# a color palette so I don't have to remember the RGB codes
red = (255,0,0)
green = (0,200,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
yellow = (255,255,0)

# list to store all of the terrain classes
terrainLines = []        

# will be used to track the lander to move the terrain appropriately
xOffset = 0
yOffset = 0

# class to hold all of the terrain lines so that they are nicer to reference
class TerrainLine():
    def draw(self):
        pygame.draw.line(screen, self.color, (self.x1 + xOffset, self.y1 + yOffset), (self.x2 + xOffset, self.y2 + yOffset), 2)

    def __init__(self, x1, y1, x2, y2, lineColor=white):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = lineColor

# function to add in a designed landing site
# looks like /\_________/\
def createLandingSite(startX, startY, lsWidth = 100, pylonHeight = 16):
    # since we create two 'pylons'
    def createPylon(startX, startY):
        endX = startX + int(pylonHeight/2)
        endY = startY - pylonHeight
        terrainLines.append(TerrainLine(startX, startY, endX, endY, yellow))
        startX = endX
        startY = endY
        endX = startX + int(pylonHeight/2)
        endY = startY + pylonHeight
        terrainLines.append(TerrainLine(startX, startY, endX, endY, yellow))
        return endX, endY

    startX, startY = createPylon(startX, startY)
    endX = startX + lsWidth
    terrainLines.append(TerrainLine(startX, startY, endX, startY, green))
    return createPylon(endX, startY)

# iterates over everything to redraw them on the new canvas
def drawAllEntities():
    screen.fill(black)
    for terrain in terrainLines:
        terrain.draw()
    pygame.display.update()

# function that controls everything happening in each update loop, movement, collision, etc.
def step():
    drawAllEntities()
    pygame.time.Clock().tick(24)

# creates the terrain randomly
def createTerrain(maxX, maxY):
    # using a function that very heavily weights the points lower than higher
    def calcY(i):
        return ((1.1**i)/1000) / ((1.1**100)/1000) * maxY
    
    hasLandingSite = False

    # loop that creates terrain until the far end of the level is reached
    while len(terrainLines) == 0 or endX < maxX:
        if len(terrainLines) == 0:
            startX = 0
            startY = frame_h - calcY(random.randint(0,100))
        endX = min((random.random()/10 * maxX) + startX, maxX)
        endY = frame_h - calcY(random.randint(0,100))
        print((startX, startY), (endX, endY))
        terrainLines.append(TerrainLine(startX, startY, endX, endY))
        startX = endX
        startY = endY

        # Creates the target landing site to win
        if (random.random() >= endX/maxX or endX >= maxX - 200) and not hasLandingSite:
            print('creating landing site')
            startX, startY = createLandingSite(startX, startY)
            hasLandingSite = True

def main():
    # designs the level
    createTerrain(1000, 400)
    
    # Event loop
    while 1:

        step()
        for event in pygame.event.get():
            # if the red 'X' button is pressed
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

if __name__ == '__main__':
    # Initialise screen
    pygame.init()
    #                                       w, h
    screen = pygame.display.set_mode((frame_w, frame_h))
    pygame.display.set_caption('Lines')
    
    screen.fill(black)
    main()