#Bandar Al Aish
#main game code

#todo list:
#add comments so it's readable (duh)
#Cactus generated by server and not players
#More players can play at the same time
#Spacebar held frames for jump height
#FIX DISTANCE BETWEEN CACTI WITH ABS()

#Game music by: Lee

from http import server
import pygame
from Player import *
from cactus import *

from pygame.constants import MOUSEBUTTONDOWN

player = Player()

pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("MultiplayerDinosaur")

#fonts
font = pygame.font.Font('freesansbold.ttf',25)
menuFont = pygame.font.Font('Sprites/Fonts/menuFont.ttf', 15)
titleFont = pygame.font.Font("Sprites/Fonts/menuFont.ttf", 35)
dinoNameFont = pygame.font.Font('Sprites/Fonts/menuFont.ttf', 10)

titleTextTop = titleFont.render("Multiplayer", True, (0,0,0))
titleTextBottom = titleFont.render("Dino", True, (0,0,0))

OfflineText = menuFont.render("Offline", True, (255,255,255))
changeDinoText = menuFont.render("Change", True, (255,255,255))
OnlineText = menuFont.render("Online", True, (255,255,255))


gameState = "mainMenu"

backgroundImage = pygame.image.load("Sprites/Background/FullBackground.png")

animationFrame = 0

displayedSprites = [dinoChoices[i][1] for i in range(len(dinoChoices))] #list comprehension, adds the second item in every array within the larger array

#sounds
soundVolume = 0.4

jumpSound = pygame.mixer.Sound("Sound/Sound effects/LVLDJUMP.wav")
jumpSound.set_volume(soundVolume)
deathSound = pygame.mixer.Sound("Sound/Sound effects/LVLDDEATH.wav")
deathSound.set_volume(soundVolume)

pygame.mixer.music.set_volume(soundVolume)

#Sets up FPS manager to keep it at 30 always
fpsClock = pygame.time.Clock()
FPS = 30

def arrToString(arr):
    for i in range(len(arr)):
        arr[i] = str(arr[i])

    return ",".join(arr)

def stringToArr(str):
    return str.split(",")

def mousePressed(x, y, width, height):
    if pygame.mouse.get_pos()[0] > x and pygame.mouse.get_pos()[0] < x+width: #Checks if x is in between the left and the right of the object
        if pygame.mouse.get_pos()[1] > y and pygame.mouse.get_pos()[1] < y+height: #Checks if y is in between the top and the bottom of the object
            return True
        else:
            return False
    else:
        return False


def offline():
    
    #Creates all cacti objects and stores them in a list
    cacti = [Cactus(-1000, i) for i in range(3)] #-1000 so it autmoatically gets moved to the beginning


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

        if gameSpeed <= 3:
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
        #pygame.draw.line(screen,(0,0,0),(0,550),(1280,550))    Line representing ground
    
        for cactus in cacti:
            cactus.draw(screen)

        pygame.display.update()
        
        #sets FPS to certain value
        fpsClock.tick(FPS)

        #Collision detection AFTER drawing so no visual bugs happen
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

def online():

    cacti = [Cactus(-1000, i) for i in range(3)] #Array of random cacti so it can be changed

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

        if gameState == "game":
            score += int(gameSpeed)
        scoreText = font.render(str(score), True, (0,0,0))

        serverData = stringToArr(player.n.send(arrToString([round(player.yPos), player.currentDino]))) #sends data as a string, gets back data and converts back to array
        onlineGameState = serverData[0]
        p2Pos = serverData[1]
        p2Dino = serverData[2]

        for i in range(len(cacti)):
            cacti[i].x = int(serverData[i+3])

        if onlineGameState == "game":
            if gameSpeed <= 3:
                gameSpeed += 0.001

        #Input handling
        if player.state == "alive":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                if player.isJump == False:
                    pygame.mixer.Sound.play(jumpSound)
                    player.yVel = 30
                    player.isJump = True

        if keys[pygame.K_DOWN]:
                player.yVel = (player.yVel - 30)*0.7 #-30 part so it's always positive and falls down


        #dino animation
        if gameState == "game":
            animationFrame += 1

        #CLEAR SCREEN          ALL DRAWNIG MUST GO BELOW HERE! VVVVVVV

        #background drawing
        screen.blit(backgroundImage, ((-animationFrame)*gameSpeed,0))
        screen.blit(backgroundImage, ((-animationFrame)*gameSpeed+2560,0)) #second image behind first one so it isnt white

        if animationFrame*gameSpeed >= 2560: #so that the background is infinte and will move back to beginning
            animationFrame = 0
    
        if animationFrame % 4 == 0:    #If statement so every new frame, the sprite is changed
            currentSpriteP2 = pygame.image.load(dinoChoices[int(p2Dino)][0])
        elif animationFrame % 4 == 1:
            currentSpriteP2 = pygame.image.load(dinoChoices[int(p2Dino)][1])
        elif animationFrame % 4 == 2:
            currentSpriteP2 = pygame.image.load(dinoChoices[int(p2Dino)][2])
        else:
            currentSpriteP2 = pygame.image.load(dinoChoices[int(p2Dino)][1])

        #sprite drawings
        screen.blit(currentSpriteP2, (200,int(p2Pos)))

        player.draw(animationFrame, screen)

        screen.blit(scoreText, (1100, 25))

        if "countdown" in onlineGameState:
            player.state = "alive"
            countdownText = titleFont.render(str(3-int(onlineGameState[-1])), True, (0,0,0))
            screen.blit(countdownText, (640, 360))
    
        for cactus in cacti:
            cactus.draw(screen)

        pygame.display.update()
        
        #sets FPS to certain value
        fpsClock.tick(FPS)

        #Collisioin detection AFTER drawing so no visual bugs happen
        for cactus in cacti:
            if cactus.collided(player.yPos) == True:
                player.yPos = -150 #teleported to 150 to indicate death
                player.state = "dead"
                pygame.mixer.Sound.play(deathSound)
                pygame.mixer.music.play(-1)
            
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

    if player.currentDino == 12:
        pygame.draw.line(screen, (255,0,0),(90,440),(90,560), width = 3)
        pygame.draw.line(screen, (255,0,0),(90,440),(210,440), width = 3)
        pygame.draw.line(screen, (255,0,0),(210,440),(210,560), width = 3)
        pygame.draw.line(screen, (255,0,0),(90,560),(210,560), width = 3)


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

            if mousePressed(100, 450, 100, 100):
                player.currentDino = 12

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

    pygame.draw.rect(screen, (255,255,255), ((1280/2)-210, 180, 420, 390)) #white rectangle behind all text

    pygame.draw.rect(screen, (100,100,100), ((1280/2)-(100/2), 310, 100, 50)) #Offline play button button
    pygame.draw.rect(screen, (100,100,100), ((1280/2)-(100/2), 400, 100, 50)) #Online play button button
    pygame.draw.rect(screen, (100,100,100), ((1280/2)-(100/2), 490, 100, 50)) #dino customization button

    screen.blit(titleTextTop, ((1280/2)-190, 200))  #title text "multiplayer" part
    screen.blit(titleTextBottom, ((1280/2)-70, 240))  #title text "dino" part
    screen.blit(OfflineText, ((1280/2)-(100/2), (720/2)-35)) #Offline play text on button
    screen.blit(changeDinoText, ((1280/2)-(100/2)+5, 415)) #change dino text on the button
    screen.blit(OnlineText, ((1280/2)-(100/2)+5, 505)) #Offline play text on button

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            #checks if mouse is in between those x values (where the box is)
            if mousePressed((1280/2)-(100/2), (720/2)-50, 100, 50):
                gameState = "playOffline"

            elif mousePressed((1280/2)-(100/2), 415, 100, 50):
                pygame.mixer.music.load("Sound/Music/DinoCustomization.mp3")
                pygame.mixer.music.play(-1) #-1 plays it infinitely
                gameState = "dinoCustomization"

            elif mousePressed((1280/2)-(100/2)+5, 505, 100, 50):
                gameState = "playOnline"

            else:
                gameState = "mainMenu"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if gameState == "playOffline":
        offline()
        gameState = "mainMenu"

    if  gameState == "playOnline":
        player.online()
        online()
        gameState = "mainMenu"
        
    if gameState == "mainMenu":
        mainMenu()

    if gameState == "dinoCustomization":
        dinoCustomization()