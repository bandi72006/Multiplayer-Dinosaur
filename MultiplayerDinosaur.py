#todo list:
#add comments so it's readable (duh)
#Collision is wack sometimes, needs to be fixed
#Add a quit button to death screen
#Sprites/animations:
#    .RGB Dino
#Spacebar held frames for jump height
#Add speed cap

#Game music by: Lee

import pygame
import random
from pygame import mouse

from pygame.constants import MOUSEBUTTONDOWN

pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("MultiplayerDinosaur")

font = pygame.font.Font('freesansbold.ttf',25)
menuFont = pygame.font.Font('Sprites/Fonts/menuFont.ttf', 20)
retryText = menuFont.render("Retry", True, (255,255,255))

gameState = "deathMenu"

dinoChoices = [["Sprites/Dinosaur/DefaultDino1.png","Sprites/Dinosaur/DefaultDino2.png","Sprites/Dinosaur/DefaultDino3.png"], #Normal/default dino
["Sprites/Dinosaur/AussieDino1.png", "Sprites/Dinosaur/AussieDino2.png", "Sprites/Dinosaur/AussieDino3.png"],  #Aussie dino
["Sprites/Dinosaur/E-Dino1.png", "Sprites/Dinosaur/E-Dino2.png", "Sprites/Dinosaur/E-Dino3.png"], #E-dino
["Sprites/Dinosaur/CocktailDino1.png", "Sprites/Dinosaur/CocktailDino2.png", "Sprites/Dinosaur/CocktailDino3.png", ], #cocktail dino
["Sprites/Dinosaur/DolphinDino1.png", "Sprites/Dinosaur/DolphinDino2.png", "Sprites/Dinosaur/DolphinDino1.png", ], #dolphin dino
["Sprites/Dinosaur/SpiderDino1.png", "Sprites/Dinosaur/SpiderDino2.png", "Sprites/Dinosaur/SpiderDino3.png"], #spider dino
["Sprites/Dinosaur/GhostDino1.png", "Sprites/Dinosaur/GhostDino2.png", "Sprites/Dinosaur/GhostDino1.png"], #ghost dino
["Sprites/Dinosaur/MLGDino1.png", "Sprites/Dinosaur/MLGDino2.png", "Sprites/Dinosaur/MLGDino3.png"]
]
currentDino = 0

displayedSprites = [dinoChoices[i][1] for i in range(len(dinoChoices))] #list comprehension, adds the second item in every array within the larger array

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
  
    def move(self, cacti, speed):
        if (self.x+self.type[0]) < 0:  # +self.type[0] part so it waits until it's completely off screen then moves it back
            self.x = 1280

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

    
def Jump(yValue, Vel, isjumpbool):
    #CREDITS TO: AndSans for the jumping mechanics!

    if isjumpbool == True:
        if yValue < 451: #One more than the ground level
            Vel -= 2
            yValue -= Vel  
    
    else:
        yValue = 450          
    
    return yValue, Vel

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
    yPos = 450
    isJump = False
    yVel = 0
    score = 0 
    run = True
    animationFrame = 1
    gameSpeed = 1

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
            cactus.move(cacti, gameSpeed)

        score += int(gameSpeed)
        scoreText = font.render(str(score), True, (0,0,0))
        highScoreText = font.render(str(highScore), True, (0,0,0))

        gameSpeed += 0.001

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
        if animationFrame % 4 == 0:    #If statement so every new frame, the sprite is changed
            currentSprite = pygame.image.load(dinoChoices[currentDino][0])
        elif animationFrame % 4 == 1:
            currentSprite = pygame.image.load(dinoChoices[currentDino][1])
        elif animationFrame % 4 == 2:
            currentSprite = pygame.image.load(dinoChoices[currentDino][2])
        else:
            currentSprite = pygame.image.load(dinoChoices[currentDino][1])

        screen.fill((255,255,255)) 
        screen.blit(currentSprite, (200, yPos))
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
    
def dinoCustomization():

    global gameState
    global currentDino

    screen.fill((255,255,255)) 

    y = 1
    x = 0

    for i in range(len(displayedSprites)):
        currentSprite = pygame.image.load(displayedSprites[i])
        screen.blit(currentSprite, ((x*200)+100, y*110))   #200 pixels between each dino + 100 offset from edge of screen
        x += 1
        if (x*200)+100 > 1280:
            y += 1
            x = 0

    pygame.draw.rect(screen, (255, 0, 0), (10, 10, 50, 50)) #exit button

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            #exit button code
            if mousePressed(10, 10, 50, 50):
                gameState = "deathMenu"

            #A bunch of if statements checking if mouse is clicked on certain dino
            if mousePressed(100, 110, 100, 100):
                currentDino = 0 
                print(currentDino)

            if mousePressed(300, 110, 100, 100):
                currentDino = 1 
                print(currentDino)

            if mousePressed(500, 110, 100, 100):
                currentDino = 2 
                print(currentDino)

            if mousePressed(700, 110, 100, 100):
                currentDino = 3 
                print(currentDino)

            if mousePressed(900, 110, 100, 100):
                currentDino = 4 
                print(currentDino)

            if mousePressed(1100, 110, 100, 100):
                currentDino = 5
                print(currentDino)

            if mousePressed(100, 220, 100, 100):
                currentDino = 6
                print(currentDino)

            if mousePressed(300, 220, 100, 100):
                currentDino = 7
                print(currentDino)



    pygame.display.update()



def deathMenu():
    global gameState

    screen.fill((255,255,255)) 
    pygame.draw.rect(screen, (100,100,100), ((1280/2)-(100/2), (720/2)-50, 100, 50)) #replay button
    pygame.draw.rect(screen, (100,100,100), ((1280/2)-(100/2), 720/2+10, 100, 50)) #dino customization button
    screen.blit(retryText, ((1280/2)-(100/2), (720/2)-35)) #retry text on button

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            #checks if mouse is in between those x values (where the box is)
            if mousePressed((1280/2)-(100/2), (720/2)-50, 100, 50):
                gameState = "play"

            elif mousePressed((1280/2)-(100/2), 720/2+10, 100, 50):
                gameState = "dinoCustomization"

            else:
                gameState = "deathMenu"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if gameState == "play":
        main()
        gameState = "deathMenu"
        
    if gameState == "deathMenu":
        deathMenu()

    if gameState == "dinoCustomization":
        dinoCustomization()
