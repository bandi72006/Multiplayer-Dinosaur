#todo list:
#Implement isJumped condition (boolean value)
#added comments so it's readable (duh)

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
isJump = False
jumpCounter = 1

#Sets up FPS manager to keep it at 60 always
fpsClock = pygame.time.Clock()
FPS = 30

def Jump(yValue, jump):
    if isJump == True:
        if jump <= 5: #max jump height
            yValue -= (1/jump*2)*50
        elif jump >= 10 and jump <= 15:
            yValue += (jump-10)*15
        else:
            jump = 1

    else:
        jump = 1

    return yValue
        
run = True

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    yPos = Jump(yPos, jumpCounter)
    jumpCounter += 1
    if jumpCounter > 15:
        isJump = False
    print(isJump)


    #Input handling
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if isJump == False:
            isJump = True
            jumpCounter = 1

    #drawing stuff    
    screen.fill((255,255,255)) 
    pygame.draw.rect(screen, (0,0,0), (250, yPos, 10, 10))
     
    pygame.display.update()
    
    #sets FPS to certain value
    fpsClock.tick(FPS)

pygame.quit()
