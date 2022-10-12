import pygame
pygame.font.init()
pygame.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))  # setting up a window with the said width and height
pygame.display.set_caption("Client")

class alien(): # making an alien class with basic python initializations
    def __init__(self, x, y, width, height, color): # alien constructor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3

    def draw(self, win):     # attribute of alien object to draw the alien
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):  # attribute of alien object to move the alien
     keys = pygame.key.get_pressed()
     if keys[pygame.K_LEFT]:
        self.x -= self.vel
     if keys[pygame.K_RIGHT]:
        self.x += self.vel
     if keys[pygame.K_UP]:
        self.y -= self.vel
     if keys[pygame.K_DOWN]:
        self.y += self.vel

     self.rect = (self.x, self.y, self.width, self.height)

def redrawWindow(win, alien):
    win.fill((0, 0, 0)) # starting with a black window (space theme)
    alien.draw(win)
    pygame.display.update()

def main(): # our main function
    run = True
    a = alien(40,40, 50, 50, (0,255,0)) # draw the alien
    clock= pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        a.move() # call the alien with move
        redrawWindow(win, a) # draw the window

main() # call main
