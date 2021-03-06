#Bandar Al Aish
#main game code

#todo list:
#add comments so it's readable (duh)
#Add box around chosen dino
#Sprites/animations:
#    .RGB Dino
#Spacebar held frames for jump height
#Add speed cap
#FIX DISTANCE BETWEEN CACTI WITH ABS()

#Game music by: Lee

import pygame
import random
from Player import *
player = Player()

from pygame.constants import MOUSEBUTTONDOWN

pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("MultiplayerDinosaur")

font = pygame.font.Font('freesansbold.ttf',25)
menuFont = pygame.font.Font('Sprites/Fonts/menuFont.ttf', 17)
titleFont = pygame.font.Font("Sprites/Fonts/menuFont.ttf", 35)
dinoNameFont = pygame.font.Font('Sprites/Fonts/menuFont.ttf', 10)
titleTextTop = titleFont.render("Multiplayer", True, (0,0,0))
titleTextBottom = titleFont.render("Dino", True, (0,0,0))

retryText = menuFont.render("Play", True, (255,255,255))
changeDinoText = menuFont.render("Change", True, (255,255,255))

gameState = "mainMenu"

backgroundImage = pygame.image.load("Sprites/Background/FullBackground.png")

animationFrame = 0

displayedSprites = [dinoChoices[i][1] for i in range(len(dinoChoices))] #list comprehension, adds the second item in every array within the larger array

#sounds
jumpSound = pygame.mixer.Sound("Sound/Sound effects/LVLDJUMP.wav")
deathSound = pygame.mixer.Sound("Sound/Sound effects/LVLDDEATH.wav")

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
  
    def move(self, cacti, speed):
        if (self.x+self.type[0]) < -10:  # +self.type[0] part so it waits until it's completely off screen then moves it back
            self.x = 1500

            for cactus in cacti:
                if cactus == self:
                        continue   #if it starts to check with itself, it goes back to beggining of loop

                while ((self.x - cactus.x) < 1000 and (self.x - cactus.x) > -1000) == True:  #checks if distance between 2 cacti is in between 1000 and -1000 (any distance within 1000 pixels)
                    self.x += random.randint(1000,3000)  #random added x value so there are gaps between each cactus
                    self.type = random.choice(self.cactiTypes)
                    self.y = 550 - self.type[1]

        self.x -= 20*speed

    def collided(self, dinoY):
        if (dinoY+100) > self.y: #+100 for the height of dino
            if(self.x > 200-self.type[0] and self.x < 300):  #200-300 because dino is always there
                return True
        
        return False
        

    def draw(self):
        pygame.draw.rect(screen, (100,255,100), (self.x, self.y, self.type[0], self.type[1]))


def mousePressed(x, y, width, height):
    if pygame.mouse.get_pos()[0] > x and pygame.mouse.get_pos()[0] < x+width: #Checks if x is in between the left and the right of the object
        if pygame.mouse.get_pos()[1] > y and pygame.mouse.get_pos()[1] < y+height: #Checks if y is in between the top and the bottom of the object
            return True
        else:
            return False
    else:
        return False


def main():
    
    #Creates all cacti objects and stores them in a list
    cacti = [cactusObject(-1000, i) for i in range(3)] #-1000 so it autmoatically gets moved to the beginning

    #sets some important variables
    score = 0 
    run = True
    animationFrame = 1
    gameSpeed = 1

    highScoreFile = open("highScoreFile.txt", "r")
    highScore = highScoreFile.read()
    highScoreFile.close()


    pygame.mixer.music.load('Sound/Music/BeepBox-Song.mp3')
    pygame.mixer.music.play(-1) #-1 plays it infinitely

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        #Movement

        player.jump()

        score += int(gameSpeed)
        scoreText = font.render(str(score), True, (0,0,0))
        highScoreText = font.render(str(highScore), True, (0,0,0))

        for cactus in cacti:
            cactus.move(cacti, gameSpeed)


        gameSpeed += 0.001

        #Input handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if player.isJump == False:
                pygame.mixer.Sound.play(jumpSound)
                player.yVel = 30
                player.isJump = True

        if keys[pygame.K_DOWN]:
                player.yVel = (player.yVel - 30)*0.7 #-30 part so it's always psitiive and falls down


        #dino animatioin   
        animationFrame += 1

        #CLEAR SCREEN          ALL DRAWNIG MUST GO BELOW HERE! VVVVVVV

        #background drawing
        screen.blit(backgroundImage, ((-animationFrame)*gameSpeed,0))
        screen.blit(backgroundImage, ((-animationFrame)*gameSpeed+2560,0)) #second image behind first one so it isnt white

        if animationFrame*gameSpeed >= 2560: #so that the background is infinte and will move back to beginning
            animationFrame = 0

        #sprite drawings
        player.draw(animationFrame, screen)
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
            if cactus.collided(player.yPos) == True:
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(deathSound)
                pygame.time.delay(1000)

                if score > int(highScore):
                    highScoreFile = open("highScoreFile.txt", "w")
                    highScoreFile.write(str(score))
                    highScoreFile.close()
                
                run = False
                break
    
def dinoCustomization():
    global gameState
    global animationFrame

    screen.fill((255,255,255)) 

    #scrolling background
    screen.blit(backgroundImage, (-animationFrame,0))
    screen.blit(backgroundImage, ((-animationFrame+2560),0)) #second image behind first one so it isnt white

    animationFrame += 0.5

    if animationFrame >= 2560: #so that the background is infinte and will move back to beginning
        animationFrame = 0

    y = 1
    x = 0
    for i in range(len(displayedSprites)):
        currentSprite = pygame.image.load(displayedSprites[i])
        screen.blit(currentSprite, ((x*200)+100, y*150))   #200 pixels between each dino + 100 offset from edge of screen
        dinoNameText = dinoNameFont.render(dinoChoices[i][3], True, ((0 if y < 2 else 255), (0 if y < 2 else 255), (0 if y < 2 else 255))) #Ternary operator to set correct font colour
        screen.blit(dinoNameText, ((x*200)+100, (y*150)+120)) 
        
        x += 1

        if (x*200)+100 > 1280:
            y += 1
            x = 0

    pygame.draw.rect(screen, (255, 0, 0), (10, 10, 50, 50)) #exit button

    #box around dino code
    if player.currentDino == 0:
        pygame.draw.line(screen, (255,0,0),(90,140),(90,260), width = 3)
        pygame.draw.line(screen, (255,0,0),(90,140),(210,140), width = 3)
        pygame.draw.line(screen, (255,0,0),(210,140),(210,260), width = 3)
        pygame.draw.line(screen, (255,0,0),(90,260),(210,260), width = 3)

    if player.currentDino == 1:
        pygame.draw.line(screen, (255,0,0),(290,140),(290,260), width = 3)
        pygame.draw.line(screen, (255,0,0),(290,140),(410,140), width = 3)
        pygame.draw.line(screen, (255,0,0),(410,140),(410,260), width = 3)
        pygame.draw.line(screen, (255,0,0),(290,260),(410,260), width = 3)

    if player.currentDino == 2:
        pygame.draw.line(screen, (255,0,0),(490,140),(490,260), width = 3)
        pygame.draw.line(screen, (255,0,0),(490,140),(610,140), width = 3)
        pygame.draw.line(screen, (255,0,0),(610,140),(610,260), width = 3)
        pygame.draw.line(screen, (255,0,0),(490,260),(610,260), width = 3)
    
    if player.currentDino == 3:
        pygame.draw.line(screen, (255,0,0),(690,140),(690,260), width = 3)
        pygame.draw.line(screen, (255,0,0),(690,140),(810,140), width = 3)
        pygame.draw.line(screen, (255,0,0),(810,140),(810,260), width = 3)
        pygame.draw.line(screen, (255,0,0),(690,260),(810,260), width = 3)

    if player.currentDino == 4:
        pygame.draw.line(screen, (255,0,0),(890,140),(890,260), width = 3)
        pygame.draw.line(screen, (255,0,0),(890,140),(1010,140), width = 3)
        pygame.draw.line(screen, (255,0,0),(1010,140),(1010,260), width = 3)
        pygame.draw.line(screen, (255,0,0),(890,260),(1010,260), width = 3)

    if player.currentDino == 5:
        pygame.draw.line(screen, (255,0,0),(1090,140),(1090,260), width = 3)
        pygame.draw.line(screen, (255,0,0),(1090,140),(1210,140), width = 3)
        pygame.draw.line(screen, (255,0,0),(1210,140),(1210,260), width = 3)
        pygame.draw.line(screen, (255,0,0),(1090,260),(1210,260), width = 3)

    if player.currentDino == 6:
        pygame.draw.line(screen, (255,0,0),(90,290),(90,410), width = 3)
        pygame.draw.line(screen, (255,0,0),(90,290),(210,290), width = 3)
        pygame.draw.line(screen, (255,0,0),(210,290),(210,410), width = 3)
        pygame.draw.line(screen, (255,0,0),(90,410),(210,410), width = 3)

    if player.currentDino == 7:
        pygame.draw.line(screen, (255,0,0),(290,290),(290,410), width = 3)
        pygame.draw.line(screen, (255,0,0),(290,290),(410,290), width = 3)
        pygame.draw.line(screen, (255,0,0),(410,290),(410,410), width = 3)
        pygame.draw.line(screen, (255,0,0),(290,410),(410,410), width = 3)
        
    if player.currentDino == 8:
        pygame.draw.line(screen, (255,0,0),(490,290),(490,410), width = 3)
        pygame.draw.line(screen, (255,0,0),(490,290),(610,290), width = 3)
        pygame.draw.line(screen, (255,0,0),(610,290),(610,410), width = 3)
        pygame.draw.line(screen, (255,0,0),(490,410),(610,410), width = 3)

    if player.currentDino == 9:
        pygame.draw.line(screen, (255,0,0),(690,290),(690,410), width = 3)
        pygame.draw.line(screen, (255,0,0),(690,290),(810,290), width = 3)
        pygame.draw.line(screen, (255,0,0),(810,290),(810,410), width = 3)
        pygame.draw.line(screen, (255,0,0),(690,410),(810,410), width = 3)

    if player.currentDino == 10:
        pygame.draw.line(screen, (255,0,0),(890,290),(890,410), width = 3)
        pygame.draw.line(screen, (255,0,0),(890,290),(1010,290), width = 3)
        pygame.draw.line(screen, (255,0,0),(1010,290),(1010,410), width = 3)
        pygame.draw.line(screen, (255,0,0),(890,410),(1010,410), width = 3)

    if player.currentDino == 11:
        pygame.draw.line(screen, (255,0,0),(1090,290),(1090,410), width = 3)
        pygame.draw.line(screen, (255,0,0),(1090,290),(1210,290), width = 3)
        pygame.draw.line(screen, (255,0,0),(1210,290),(1210,410), width = 3)
        pygame.draw.line(screen, (255,0,0),(1090,410),(1210,410), width = 3)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            #exit button code
            if mousePressed(10, 10, 50, 50):
                pygame.mixer.music.stop()
                gameState = "mainMenu"

            #A bunch of if statements checking if mouse is clicked on certain dino
            if mousePressed(100, 150, 100, 100):
                player.currentDino = 0 

            if mousePressed(300, 150, 100, 100):
                player.currentDino = 1 

            if mousePressed(500, 150, 100, 100):
                player.currentDino = 2 

            if mousePressed(700, 150, 100, 100):
                player.currentDino = 3 

            if mousePressed(900, 150, 100, 100):
                player.currentDino = 4 

            if mousePressed(1100, 150, 100, 100):
                player.currentDino = 5

            if mousePressed(100, 300, 100, 100):
                player.currentDino = 6

            if mousePressed(300, 300, 100, 100):
                player.currentDino = 7

            if mousePressed(500, 300, 100, 100):
                player.currentDino = 8

            if mousePressed(700, 300, 100, 100):
                player.currentDino = 9
            
            if mousePressed(900, 300, 100, 100):
                player.currentDino = 10
            
            if mousePressed(1100, 300, 100, 100):
                player.currentDino = 11

            playerSettingsFile = open("playerSettings.txt", "w")
            playerSettingsFile.write(str(player.currentDino))
            playerSettingsFile.close()



    pygame.display.update()



def mainMenu():
    global gameState
    global animationFrame

    if pygame.mixer.music.get_busy() == False:
        pygame.mixer.music.load("Sound/Music/Rock_type_beep.mp3")
        pygame.mixer.music.play(-1) #-1 plays it infinitely
    
    screen.fill((255,255,255))

    #scrolling background
    screen.blit(backgroundImage, (-animationFrame,0))
    screen.blit(backgroundImage, ((-animationFrame+2560),0)) #second image behind first one so it isnt white

    animationFrame += 0.5

    if animationFrame >= 2560: #so that the background is infinte and will move back to beginning
        animationFrame = 0

    pygame.draw.rect(screen, (255,255,255), ((1280/2)-210, 180, 420, 360)) #white rectangle behind all text

    pygame.draw.rect(screen, (100,100,100), ((1280/2)-(100/2), (720/2)-50, 100, 50)) #replay button
    pygame.draw.rect(screen, (100,100,100), ((1280/2)-(100/2), 400, 100, 50)) #dino customization button

    screen.blit(titleTextTop, ((1280/2)-190, 200))  #title text "multiplayer" part
    screen.blit(titleTextBottom, ((1280/2)-70, 240))  #title text "dino" part
    screen.blit(retryText, ((1280/2)-(100/2)+10, (720/2)-35)) #retry text on button
    screen.blit(changeDinoText, ((1280/2)-(100/2), 415)) #change dino text on the button

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            #checks if mouse is in between those x values (where the box is)
            if mousePressed((1280/2)-(100/2), (720/2)-50, 100, 50):
                gameState = "play"

            elif mousePressed((1280/2)-(100/2), 415, 100, 50):
                pygame.mixer.music.load("Sound/Music/DinoCustomization.mp3")
                pygame.mixer.music.play(-1) #-1 plays it infinitely
                gameState = "dinoCustomization"

            else:
                gameState = "mainMenu"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if gameState == "play":
        main()
        gameState = "mainMenu"
        
    if gameState == "mainMenu":
        mainMenu()

    if gameState == "dinoCustomization":
        dinoCustomization()
