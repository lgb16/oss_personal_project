import pygame,sys
from datafile import *

#declare window size
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

#initialize window
pygame.init()
pygame.display.set_caption("Simple PyGame Example")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#class for player character
class Player:
    def __init__(self):
        self.spr_player = SpriteSheet('phoenix-cc0-spritesheet.png',20,20,5,4,19) 
        self.pos_x=200
        self.pos_y=200


clock = pygame.time.Clock()

player=Player()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    key_event = pygame.key.get_pressed()
    if key_event[pygame.K_LEFT]:
        player.pos_x -=3

    if key_event[pygame.K_RIGHT]:
        player.pos_x +=3

    if key_event[pygame.K_UP]:
        player.pos_y -=3

    if key_event[pygame.K_DOWN]:
        player.pos_y +=3

    if key_event[pygame.K_w]:
        player.pos_y +=3


    screen.fill(white)
    screen.blit(player.spr_player.spr[0], (player.pos_x, player.pos_y))
    pygame.display.update()
