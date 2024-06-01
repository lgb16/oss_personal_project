import pygame,sys
from datafile import *

#initialize window
pygame.init()
pygame.display.set_caption("Simple PyGame Example")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

Font=pygame.font.Font(None,50)
start_tick = pygame.time.get_ticks()

#declare data classes for game
background_spr=SpriteSheet('Grass.png')
background_spr.get_image(0,0,size_Grass,1)
player=Player()

group_Enemy.append(Enemy(1,200,200,False))
group_Enemy.append(Enemy(2,200,300,False))
group_Enemy.append(Enemy(3,200,400,False))

def start_Game():
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
        if player.attacking == False:
            player.index=0
        player.attacking = True
    else:
        player.attacking = False

    #check collide player and enemy
    for enemy in group_Enemy:
        if pygame.sprite.collide_mask(player, enemy):
            print("collide")

    #check collide flame and ememy
    for flame in group_Flame:
        for enemy in group_Enemy:
            if pygame.sprite.collide_mask(flame, enemy):
                enemy.health-=1
                group_Flame.remove(flame)
                if enemy.health <= 0:
                    global score
                    score+=enemy.score
                    group_Enemy.remove(enemy)

    #update all classes
    for flame in group_Flame:
        flame.update()
        if flame.out_boundary:
            group_Flame.remove(flame)
    player.update()
    for enemy in group_Enemy:
        enemy.update()

    pygame.display.update()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    if start:
        start_Game()
    
    #fill screen background and scoreboard
    x=0
    y=0
    while y < SCREEN_HEIGHT:
        screen.blit(background_spr.spr[0],(x,y))
        x+=size_Grass[0]
        if x>=SCREEN_WIDTH:
            x=0
            y+=size_Grass[1]

    pygame.draw.rect(screen, black, [0,0,SCREEN_WIDTH,SCORE_HEIGHT])

    text_time=Font.render("TIME : "+str((pygame.time.get_ticks()-start_tick)//1000),True,white)
    screen.blit(text_time,(30,30))

    text_score=Font.render("SCORE : "+str(score),True,white)
    screen.blit(text_score,(900,30))
    
    #show all images
    for enemy in group_Enemy:
        screen.blit(enemy.image,(enemy.pos_x,enemy.pos_y))
    for flame in group_Flame:
        screen.blit(flame.image,(flame.pos_x,flame.pos_y))
    screen.blit(player.image,(player.pos_x,player.pos_y))

    pygame.display.update()
