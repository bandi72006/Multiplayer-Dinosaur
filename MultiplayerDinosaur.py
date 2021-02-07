#todo list:
#add comments so it's readable (duh)
#Collision is wack sometimes, needs to be fixed
#Addd a quit button to death screen a
#Sprites/animations
#Add a game speed system that relies on the score (higher score = faster)
#Spacebar held frames for jump height

#Game music by: Lee

from typing import Container
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("MultiplayerDinosaur")
defaultSprite = pygame.image.load("Sprites/Dinosaur/Dino100px2.png")

font = pygame.font.Font('freesansbold.ttf',25)
menuFont = pygame.font.Font('Sprites/Fonts/menuFont.ttf', 20)

#sounds
jumpSound = pygame.mixer.Sound("Sound/Sound effects/LVLDJUMP.wav")
deathSound = pygame.mixer.Sound("Sound/Sound effects/LVLDDEATH.wav")
pygame.mixer.music.load('Sound/Music/BeepBox-Song.mp3')

#Sets up FPS manager to keep it at 30 always
fpsClock = pygame.time.Clock()
FPS = 30

class cactusObject:
    def __init__(self, x, i):
        self.x = x - random.randint(100,1000)
        self.cactiTypes = [[40, 60], [90, 50], [20,100]]
        self.type = random.choice(self.cactiTypes)
        self.y = 550-self.type[1]
        self.order = i #important for calculating distance between each cacti
  
    def move(self, cacti):
        if (self.x+self.type[0]) < 0:  # +self.type[0] part so it waits until it's completely off screen then moves it back
            self.x = 1280

            for cactus in cacti:
                if cactus == self:
                        continue   #if it starts to check with itself, it goes back to beggining of loop

                while ((self.x - cactus.x) < 1000 and (self.x - cactus.x) > -1000) == True:  #checks if distance between 2 cacti is in between 1000 and -1000 (any distance within 1000 pixels)
                    self.x += random.randint(1000,3000)  #random added x value so there are gaps between each cactus
                    self.type = random.choice(self.cactiTypes)
                    self.y = 550 - self.type[1]

        self.x -= 20  

    def collided(self, dinoY):
        if (dinoY+100) > self.y: #+100 for the height of dino
            if(self.x > 200-self.type[0] and self.x < 300):  #200-300 because dino is always there
                return True
        
        return False
        

    def draw(self):
        pygame.draw.rect(screen, (100,255,100), (self.x, self.y, self.type[0], self.type[1]))

#def Jump(yValue, jump):
    
def Jump(yValue, Vel, isjumpbool):
    #CREDITS TO: AndSans for the jumping mechanics!

    if isjumpbool == True:
        if yValue < 451: #One more than the ground level
            Vel -= 2
            yValue -= Vel  
    
    else:
        yValue = 450          
    
    return yValue, Vel


def main():
    
    #Creates all cacti objects and stores them in a list
    cacti = [cactusObject(-1000, i) for i in range(3)] #-1000 so it autmoatically gets moved to the beginning


    #sets some important variables
    yPos = 450
    isJump = False
    yVel = 0
    score = 0 
    run = True
    animationFrame = 1

    highScoreFile = open("highScoreFile.txt", "r")
    highScore = highScoreFile.read()
    highScoreFile.close()

    pygame.mixer.music.play(-1) #-1 plays it infinitely

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        #Movement
        yPos, yVel = Jump(yPos, yVel, isJump)

        if yPos > 450: #keeps yValue always at 450, as if it hit the ground
            yPos = 450
            isJump = False

        for cactus in cacti:
            cactus.move(cacti)

        score += 1
        scoreText = font.render(str(score), True, (0,0,0))
        highScoreText = font.render(str(highScore), True, (0,0,0))

        #Input handling
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if isJump == False:
                pygame.mixer.Sound.play(jumpSound)
                yVel = 30
                isJump = True

        if keys[pygame.K_DOWN]:
                yVel = int((yVel - 30)*0.7) #-30 part so it's always psitiive and falls down


        #drawing stuff    

        animationFrame += 1
        if animationFrame % 3 == 0:    #If statement so every new frame, the sprite is changed
            defaultSprite = pygame.image.load("Sprites/Dinosaur/Dino100px1.png")
        elif animationFrame % 3 == 1:
            defaultSprite = pygame.image.load("Sprites/Dinosaur/Dino100px2.png")
        else:
            defaultSprite = pygame.image.load("Sprites/Dinosaur/Dino100px3.png")

        screen.fill((255,255,255)) 
        screen.blit(defaultSprite, (200, yPos))
        screen.blit(scoreText, (1100, 25))
        screen.blit(highScoreText, (1200, 25))
        pygame.draw.line(screen,(0,0,0),(0,550),(1280,550))
    
        for cactus in cacti:
            cactus.draw()


        #screen.blit(defaultSprite, (640, yPos)) REALLY BIG! DON'T ADD YET!

        pygame.display.update()
        
        #sets FPS to certain value
        fpsClock.tick(FPS)

        #Collisioin detection AFTER drawing so no visual bugs happen
        for cactus in cacti:
            if cactus.collided(yPos) == True:
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(deathSound)
                pygame.time.delay(1000)

                if score > int(highScore):
                    highScoreFile = open("highScoreFile.txt", "w")
                    highScoreFile.write(str(score))
                    highScoreFile.close()

                run = False
                break

def playAgain():

    retryText = menuFont.render("Retry", True, (255,255,255))

    pygame.draw.rect(screen, (0,0,0), ((1280/2)-(100/2), (720/2)-(50/2), 100, 50))
    screen.blit(retryText, ((1280/2)-(100/2), (720/2)-(50/2)+15))

    pygame.display.update()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #checks if mouse is in between those x values (where the box is)
                if pygame.mouse.get_pos()[0] > (1280/2)-(100/2) and pygame.mouse.get_pos()[0] < (1280/2)-(100/2)+100:
                    if pygame.mouse.get_pos()[1] > (720/2)-(50/2) and pygame.mouse.get_pos()[1] < (720/2)-(50/2)+50:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    if playAgain() == True:
        main()
