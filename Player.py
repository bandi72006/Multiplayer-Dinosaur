#Bandar Al Aish
#All code for the dino

import pygame

from network import Network

dinoChoices = [["Sprites/Dinosaur/DefaultDino1.png","Sprites/Dinosaur/DefaultDino2.png","Sprites/Dinosaur/DefaultDino3.png", "Default Dino"], #Normal/default dino
["Sprites/Dinosaur/AussieDino1.png", "Sprites/Dinosaur/AussieDino2.png", "Sprites/Dinosaur/AussieDino3.png", "Aussie Dino"],  #Aussie dino
["Sprites/Dinosaur/E-Dino1.png", "Sprites/Dinosaur/E-Dino2.png", "Sprites/Dinosaur/E-Dino3.png", "E-Dino"], #E-dino
["Sprites/Dinosaur/CocktailDino1.png", "Sprites/Dinosaur/CocktailDino2.png", "Sprites/Dinosaur/CocktailDino3.png", "Cocktail Dino"], #cocktail dino
["Sprites/Dinosaur/DolphinDino1.png", "Sprites/Dinosaur/DolphinDino2.png", "Sprites/Dinosaur/DolphinDino1.png", "Dolphin Dino"], #dolphin dino
["Sprites/Dinosaur/SpiderDino1.png", "Sprites/Dinosaur/SpiderDino2.png", "Sprites/Dinosaur/SpiderDino3.png", "Spider Dino"], #spider dino
["Sprites/Dinosaur/GhostDino1.png", "Sprites/Dinosaur/GhostDino2.png", "Sprites/Dinosaur/GhostDino1.png", "Ghost Dino"], #ghost dino
["Sprites/Dinosaur/MLGDino1.png", "Sprites/Dinosaur/MLGDino2.png", "Sprites/Dinosaur/MLGDino3.png", "MLG Dino"], #MLG dino
["Sprites/Dinosaur/SteveDino1.png", "Sprites/Dinosaur/SteveDino2.png", "Sprites/Dinosaur/SteveDino3.png", "Steve Dino"],  #Steve dino
["Sprites/Dinosaur/AlexDino1.png", "Sprites/Dinosaur/AlexDino2.png", "Sprites/Dinosaur/AlexDino3.png", "Alex Dino"], #Alex Dino (from minecraft)
["Sprites/Dinosaur/DreamDino1.png", "Sprites/Dinosaur/DreamDino2.png", "Sprites/Dinosaur/DreamDino3.png", "Dream Dino"], #Dream Dino (minecraft youtuber)
["Sprites/Dinosaur/AnimeDino1.png", "Sprites/Dinosaur/AnimeDino2.png", "Sprites/Dinosaur/AnimeDino3.png", "Anime Dino"], #Anime Dino
["Sprites/Dinosaur/MarioDino1.png", "Sprites/Dinosaur/MarioDino2.png", "Sprites/Dinosaur/MarioDino3.png", "Mario Dino"], #Mario Dino
]

n = Network() 

class Player():
    def __init__(self):
        self.yPos = 450
        self.isJump = False
        self.yVel = 0
        self.currentSprite = 0
        self.state = "alive"
        
        playerSettingsFile = open("playerSettings.txt", "r")
        self.currentDino = int(playerSettingsFile.readline())
        playerSettingsFile.close()


    def jump(self):
        #CREDITS TO: AndSans for the jumping mechanics!

        if self.isJump == True:
            if self.yPos < 451: #One more than the ground level
                self.yVel -= 2
                self.yPos -= self.yVel  
        
        else:
            if self.state == "alive":
                self.yPos = 450  


        if self.yPos > 450: #keeps yValue always at 450, as if it hit the ground
            self.yPos = 450
            self.isJump = False


    def draw(self, frame, screen):
        #Animation code
        if frame % 4 == 0:    #If statement so every new frame, the sprite is changed
            self.currentSprite = pygame.image.load(dinoChoices[self.currentDino][0])
        elif frame % 4 == 1:
            self.currentSprite = pygame.image.load(dinoChoices[self.currentDino][1])
        elif frame % 4 == 2:
            self.currentSprite = pygame.image.load(dinoChoices[self.currentDino][2])
        else:
            self.currentSprite = pygame.image.load(dinoChoices[self.currentDino][1])  


        screen.blit(self.currentSprite, (200, self.yPos))    


        

