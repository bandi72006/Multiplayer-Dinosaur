#todo list:
#Implement isJumped condition (boolean value)
#add comments so it's readable (duh)
#Make jumping smoother (not linear)

import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("MultiplayerDinosaur")
defaultSprite = pygame.image.load("Sprites/Dinosaur/Dinosaur.png")

#sets some important variables
yPos = 500
yVel = 0
isJump = False
jumpCounter = 1
jumpHeight = 20

#Sets up FPS manager to keep it at 60 always
fpsClock = pygame.time.Clock()
FPS = 30

class cactusObject(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(1,3)
        self.width = 20 
        self.height = 50
  
    def move(self):
        if self.x < 0:
            self.x = 500
        self.x -= 5

    def collided(self, dinoY):
        print(dinoY+50, self.y)
        if (dinoY+50) > self.y:
            if(self.x > 200 and self.x <250):
                return True
        
        return False
        

    def draw(self):
        pygame.draw.rect(screen, (100,255,100), (self.x, self.y, self.width, self.height))



cactus = cactusObject(1280, 500)


def Jump(yValue, jump):
    if isJump == True:
        #jump maths (linear for now)
        if jump <= 10: #max jump height
            yValue -= 20
        elif jump > 10 and jump <= jumpHeight:
            if yValue < 500:
                yValue += 20
            
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


    #Movement
    yPos = Jump(yPos, jumpCounter)
    jumpCounter += 1
    if jumpCounter > jumpHeight: #5 extra frames for a tiny delay
        isJump = False

    cactus.move()

    cactus.collided(yPos)



    #Input handling
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        if isJump == False:
            isJump = True
            jumpCounter = 1

    #drawing stuff    
    screen.fill((255,255,255)) 
    pygame.draw.rect(screen, (0,0,0), (200, yPos, 50, 50))
    cactus.draw()
    pygame.draw.line(screen,(0,0,0),(0,550),(1280,550))

    #screen.blit(defaultSprite, (640, yPos)) REALLY BIG! DON'T ADD YET!

    pygame.display.update()
    
    #sets FPS to certain value
    fpsClock.tick(FPS)

pygame.quit()
