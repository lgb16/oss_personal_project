import pygame,sys
from datafile import *

#initialize window
pygame.init()
pygame.display.set_caption("Simple PyGame Example")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

Font=pygame.font.Font(None,50)
start_tick = pygame.time.get_ticks()

background_spr=SpriteSheet('Grass.png',Grass_WIDTH,Grass_HEIGHT,1,1,1)
player=Player()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    key_event = pygame.key.get_pressed()
    if key_event[pygame.K_LEFT]:
        player.fliped=False
        player.pos_x -=3

    if key_event[pygame.K_RIGHT]:
        player.fliped=True
        player.pos_x +=3

    if key_event[pygame.K_UP]:
        player.pos_y -=3

    if key_event[pygame.K_DOWN]:
        player.pos_y +=3

    if key_event[pygame.K_a]:
        player.attacking = True
    else:
        player.attacking = False

    #fill screen with Grass and scoreboard
    x=0
    y=0
    while y < SCREEN_HEIGHT:
        screen.blit(background_spr.spr[0],(x,y))
        x+=Grass_WIDTH
        if x >= SCREEN_WIDTH:
            x=0
            y+=Grass_HEIGHT
  
    pygame.draw.rect(screen, black, [0,0,SCREEN_WIDTH,SCORE_HEIGHT])

    text_time=Font.render("TIME : "+str((pygame.time.get_ticks()-start_tick)//1000),True,white)
    screen.blit(text_time,(30,30))

    #show player and enemies
    player.update()
    screen.blit(player.image, (player.pos_x, player.pos_y))
    
    pygame.display.update()
