#Christianne Maene
import pygame, sys
from pygame import mixer
from pygame.locals import *
import pickle
import select
import socket
import random
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
WIDTH = 1000
HEIGHT = 800
BUFFERSIZE = 4096
#define colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
bg = pygame.image.load("images/space.jpg")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders')
#define fonts
font40 = pygame.font.SysFont('Constantia', 40)
clock = pygame.time.Clock()

serverAddr = '192.168.1.67'
if len(sys.argv) == 2:
 serverAddr = sys.argv[1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverAddr, 4330))

sprites1 = pygame.image.load('images/alien1.png')
sprites2 = pygame.image.load('images/alien2.png')
sprites3 = pygame.image.load('images/alien3.png')
sprites4 = pygame.image.load('images/alien4.png')
sprites5 = pygame.image.load('images/alien5.png')



spaceshipSprite1= pygame.image.load('images/spaceship.png')
laser_fx = pygame.mixer.Sound("images/laser.wav")
laser_fx.set_volume(0.25)
explosion_fx = pygame.mixer.Sound("images/explosion.wav")
explosion_fx.set_volume(0.25)

spaceship_cooldown = 100#bullet cooldown in milliseconds
last_spaceship_shot = pygame.time.get_ticks()
playerid = 0

sprites = { 0: sprites1, 1: sprites2, 2:sprites3, 3:sprites4, 4:sprites5 }
explosion_group = pygame.sprite.Group()
#create Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"images/explosion.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            #add the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
    def update(self):
        explosion_speed = 3
        #update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #if the animation is complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

class Alien(pygame.sprite.Sprite):
  def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/alien1.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
        self.id = id


  def update(self):
        if self.id == 0:
           self.id = playerid
        #set movement speed
        speed = 3
        #set a cooldown variable
        cooldown = 500 #milliseconds
        game_over = 0


        #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += speed
        if key[pygame.K_UP] and self.rect.left > 0:
            self.rect.y -= speed
        if key[pygame.K_DOWN] and self.rect.right < WIDTH:
            self.rect.y += speed



        #record current time
        time_now = pygame.time.get_ticks()
        #shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            laser_fx.play()
            Alienbullet_group.add(bullet)
            self.last_shot = time_now


        #update mask
        self.mask = pygame.mask.from_surface(self.image)


        #draw health bar
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.top - 25), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.top - 25), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        elif self.rect.y ==HEIGHT:
            game_over = 2
        return game_over
  def render(self):
    screen.blit(self.image, (self.rect.x, self.rect.y))


class GameEvent:
 def __init__(self, vx, vy):
   self.vx = vx
   self.vy = vy
class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.rect.x=x
        self.rect.y=y
    def update(self):
        self.rect.y += 2
        if self.rect.top > HEIGHT:
            self.kill()

cc = Alien(200, 50, 3)
bullet = AlienBullet(cc.rect.centerx, cc.rect.top)
alien_group = pygame.sprite.Group()
alien_group.add(cc)
#create Bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 2
        if self.rect.top > HEIGHT:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, False, pygame.sprite.collide_mask):
            self.kill()
            explosion_fx.play()
            #reduce spaceship health
            cc.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)




#create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
Alienbullet_group = pygame.sprite.Group()

class Spaceships(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1
        self.health = 10
        self.health_remaining= self.health


    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 4
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
        if pygame.sprite.spritecollide(self, Alienbullet_group, False, pygame.sprite.collide_mask):
            #reduce spaceship health
            self.health_remaining -= 1
            if self.health_remaining <=0:
                self.kill()
                explosion_fx.play()
                explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
                explosion_group.add(explosion)
cols=10
rows= 5
def create_spaceships():
    #generate aliens
    for row in range(rows):
        for item in range(cols):
            spaceship = Spaceships(50 + item * 100, 450 + row * 70)
            spaceship_group.add(spaceship)

create_spaceships()
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
minions =[]
while True:
 time_now = pygame.time.get_ticks()
 ins, outs, ex = select.select([s], [], [], 0)
 for inm in ins:
   gameEvent = pickle.loads(inm.recv(BUFFERSIZE))
   if gameEvent[0] == 'id update':
     playerid = gameEvent[1]
     if time_now>40000:
         print(playerid)
   if gameEvent[0] == 'player locations':
     gameEvent.pop(0)
     minions = []
     for minion in gameEvent:
       if minion[0] != playerid:
         minions.append(Alien(minion[1], minion[2], minion[0]))



 for event in pygame.event.get():
   if event.type == QUIT:
      pygame.quit()
      sys.exit()
   if event.type == KEYDOWN:
     if event.key == K_LEFT: cc.vx = -7
     if event.key == K_RIGHT: cc.vx = 7
     if event.key == K_UP: cc.vy = -7
     if event.key == K_DOWN: cc.vy = 7
   if event.type == KEYUP:
     if event.key == K_LEFT and cc.vx == -7: cc.vx = 0
     if event.key == K_RIGHT and cc.vx == 7: cc.vx = 0
     if event.key == K_UP and cc.vy == -7: cc.vy = 0
     if event.key == K_DOWN and cc.vy == 7: cc.vy = 0



 clock.tick(60)
 screen.blit(bg, (0, 0))

 cc.update()
 time_now = pygame.time.get_ticks()
 if len(spaceship_group) != 0:
     if time_now - last_spaceship_shot > spaceship_cooldown:
         laser_fx.play()
         spaceship = random.choice(spaceship_group.sprites())
         spaceship_bullet = Bullets(spaceship.rect.centerx, spaceship.rect.top)
         bullet_group.add(spaceship_bullet)
         last_spaceship_shot = time_now


 #check if all the aliens have been killed
 if len(alien_group) == 0:

     draw_text('GAME OVER!', font40, white, int(WIDTH / 2 - 100), int(HEIGHT / 2 + 50))

 else:
    if len(spaceship_group) == 0:

        draw_text('You Win!', font40, white, int(WIDTH / 2 - 100), int(HEIGHT / 2 + 50))



 spaceship_group.draw(screen)
 bullet_group.draw(screen)
 explosion_group.draw(screen)
 Alienbullet_group.draw(screen)
 spaceship_group.update()
 bullet_group.update()
 alien_group.update()
 explosion_group.update()
 Alienbullet_group.update()




 for m in minions:
     m.render()
     cc.update()

 pygame.display.update()


 ge = ['position update', playerid, cc.rect.x, cc.rect.y, cc.update(), bullet.update(), bullet.rect.centerx, bullet.rect.centery]


 s.send(pickle.dumps(ge))
s.close()


