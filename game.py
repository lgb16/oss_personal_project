import pygame,sys,time
from datafile import *

#initialize window
pygame.init()
pygame.display.set_caption("Simple PyGame Example")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

Font=pygame.font.Font(None,50)

#declare data classes for game
background_spr=SpriteSheet('Grass.png')
background_spr.get_image(0,0,size_Grass,1)
player=Player()

group_Enemy.append(Enemy(1,200,200,False))
group_Enemy.append(Enemy(2,200,300,False))
group_Enemy.append(Enemy(3,200,400,False))

score = 0
start_tick = 0
Time = 0
start=False
end=False

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
            global start, end
            start=False
            end=True

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

def reset():
    global player, group_Enemy, group_Flame
    del group_Enemy[0:]
    del group_Flame[0:]
    player.reset()

while True:
    clock.tick(60)

    if start and not end:
        Time=pygame.time.get_ticks()-start_tick
        start_Game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not start and end:
                    end=False
                    reset()
                start_tick=pygame.time.get_ticks()
                start=True
    '''
    if start==True:
        Time=pygame.time.get_ticks()-start_tick
        start_Game()
    '''
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

    text_time=Font.render("TIME : "+str(Time//1000),True,white)
    screen.blit(text_time,(30,30))

    text_score=Font.render("SCORE : "+str(score),True,white)
    screen.blit(text_score,(900,30))
    
    #show all images
    for enemy in group_Enemy:
        screen.blit(enemy.image,(enemy.pos_x,enemy.pos_y))
    for flame in group_Flame:
        screen.blit(flame.image,(flame.pos_x,flame.pos_y))
    screen.blit(player.image,(player.pos_x,player.pos_y))

    if not start and not end:
        text_start=Font.render("Press Spacebar to start!", True , black)
        screen.blit(text_start,(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2-100))
    elif not start and end:
        text_end=Font.render("Game Over!",True,black)
        screen.blit(text_end,(SCREEN_WIDTH//2-80,SCREEN_HEIGHT//2-200))
        text_end2=Font.render("Score : "+str(score),True,black)
        screen.blit(text_end2,(SCREEN_WIDTH//2-50,SCREEN_HEIGHT//2-100))
        text_end3=Font.render("Press Spacebar to restart!",True,black)
        screen.blit(text_end3,(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2))
    pygame.display.update()
