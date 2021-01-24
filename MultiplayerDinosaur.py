#todo list:
#Implement isJumped condition (boolean value)

import pygame
import random

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("MultiplayerDinosaur")

#sets some important variables
xPos = 250
yPos = 250
xVel = 0
yVel = 0

#Sets up FPS manager to keep it at 60 always
fpsClock = pygame.time.Clock()
FPS = 30


def Jump(yValue):
    if (yValue > 200): #200 = height of jump
        for i in range(50):
            yValue = yValue - 1
            print(yValue)
            return yValue

    return yValue


run = True

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Input handling
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        yPos = Jump(yPos)

    #drawing stuff    
    screen.fill((255,255,255)) 
     
    pygame.display.update()
    
    #sets FPS to certain value
    fpsClock.tick(FPS)

pygame.quit()
