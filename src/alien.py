import pygame
# Creating an alien class
class Alien():
    def __init__(self, x, y, width, height, color): #alien constructor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect= (x, y, width, height)
        self.vel = 3
    def draw (self, win):  #window attrbute
        pygame.draw.rect(win, self.color, self.rect)
    def move (self): # move attribute
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel
        self.update()
    def update(self): #update attribute
        self.rect = (self.x, self.y, self.width, self.height)

