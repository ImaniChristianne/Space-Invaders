import pygame
pygame.font.init()
pygame.init()
from network import Network

width = 600 #screen width
height = 800
win = pygame.display.set_mode((width, height))  # setting up a window with the said width and height
pygame.display.set_caption("Client")

#load background stars image
bg = pygame.image.load("space.png")

def redrawWindow(win, player, player1):
    win.blit(bg,(0, 0)) # starting with a space theme
    player.draw(win) #draw first player
    player1.draw(win) #draw second player
    pygame.display.update() #update display

def main(): # our main function
    run = True
    n = Network() #from metwork
    p = n.getP()
    clock= pygame.time.Clock()

    while run:
        clock.tick(60)
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move() # call the alien with move
        redrawWindow(win, p, p2) # draw the window

main() # call main
