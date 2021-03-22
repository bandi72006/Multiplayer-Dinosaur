#Bandar Al Aish 
#All code for the cactus class

#Cactus drawn by Sasha

from os import X_OK
import pygame
import random

cactiTypes = ["Sprites/Cactus/Cactus1.png", "Sprites/Cactus/Cactus2.png", "Sprites/Cactus/Cactus2.png"]

class Cactus:
    def __init__(self, x, i):
        self.x = x - random.randint(100,1000)
        self.type = random.choice(cactiTypes)
        self.currentSprite = pygame.image.load(self.type)
        self.dimensions = self.currentSprite.get_rect().size
        self.y = 550-self.dimensions[1]
        self.order = i #important for calculating distance between each cacti
  
    def move(self, cacti, speed):
        if (self.x+self.dimensions[0]) < 0:  # +self.type[0] part so it waits until it's completely off screen then moves it back
            self.x = 1500

            for cactus in cacti:
                if cactus == self:
                        continue   #if it starts to check with itself, it goes back to beggining of loop

                while (abs(self.x-cactus.x) < 1000) == True:  #checks if distance between 2 cacti is in between 1000 and -1000 (any distance within 1000 pixels)
                    self.x += random.randint(1000,3000)  #random added x value so there are gaps between each cactus
                    self.type = random.choice(cactiTypes)
                    self.currentSprite = pygame.image.load(self.type)
                    self.dimensions = self.currentSprite.get_rect().size
                    self.y = 550 - self.dimensions[1]

        self.x -= 20*speed

    def collided(self, dinoY):
        if (dinoY+100) > self.y: #+100 for the height of dino
            if(self.x > 200-self.dimensions[0] and self.x < 300):  #200-300 because dino is always there
                return True
        
        return False
        

    def draw(self, screen):
        currentSprite = pygame.image.load(self.type)
        screen.blit(currentSprite, (self.x, self.y))