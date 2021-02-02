#todo list:
#add comments so it's readable (duh)
#Sprites/animations
#Add a game speed system that relies on the score (higher score = faster)
#Spacebar held frames for jump height

#Game music by: Lee

import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("MultiplayerDinosaur")
defaultSprite = pygame.image.load("Sprites/Dinosaur/Dino100px.png")

font = pygame.font.Font('freesansbold.ttf',25)

#sounds
jumpSound = pygame.mixer.Sound("Sound/Sound effects/LVLDJUMP.wav")
deathSound = pygame.mixer.Sound("Sound/Sound effects/LVLDDEATH.wav")
pygame.mixer.music.load('Sound/Music/BeepBox-Song.mp3')

#Sets up FPS manager to keep it at 30 always
fpsClock = pygame.time.Clock()
FPS = 30

class cactusObject:
    def __init__(self, x, y):
        self.x = x + random.randint(100,1000)
        self.y = y
        self.type = random.randint(1,3)
        self.width = 20 
        self.height = 50
  
    def move(self):
        if self.x < 0:
            self.x = 1280 + random.randint(100,1000) #random added x value so there are gaps between each cactus
        self.x -= 20

    def collided(self, dinoY):
        if (dinoY+100) > self.y:
            if(self.x > 200 and self.x <300):
                return True
        
        return False
        

    def draw(self):
        pygame.draw.rect(screen, (100,255,100), (self.x, self.y, self.width, self.height))

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
    cacti = [cactusObject(1280, 500) for i in range(3)]

    #sets some important variables
    yPos = 450
    isJump = False
    yVel = 0
    score = 0 
    run = True

    highScoreFile = open("highScoreFile.txt", "r")
    highScore = highScoreFile.read()
    highScoreFile.close()

    pygame.mixer.music.play(0)

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        #Movement
        yPos, yVel = Jump(yPos, yVel, isJump)
        if yPos > 450:
            yPos = 450
            isJump = False

        for cactus in cacti:
            cactus.move()

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
                yVel = int((yVel - 30)*1.1) #-30 part so it's always psitiive and falls down


        #drawing stuff    
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
    pygame.draw.rect(screen, (0,0,0), (1280/2, 720/2, 100, 50))
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
            else:
                return False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    if playAgain() == True:
        main()
