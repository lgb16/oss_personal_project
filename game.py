import pygame,sys,random
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

score_Enemy=[]
for i in range(3):
    score_Enemy.append(Enemy(i+1,350+i*200,0,True))

score = 0
start_tick = 0
Time = 0
last_spawn_Time = 0
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

    #add random enemy
    global last_spawn_Time
    if Time-last_spawn_Time >= 1:
        if Time >= 80:
            Type=random.randrange(1,18)//6+1
        else:
            Type=random.randrange(1,2+Time//5)//6+1

        if random.randrange(1,3)==1:
            fliped=False
            x=-size_Enemy[0]*1.5
        else:
            fliped=True
            x=SCREEN_WIDTH+size_Enemy[0]*1.5
        y=random.randrange(SCORE_HEIGHT+20,SCREEN_HEIGHT-size_Enemy[1]-20)

        group_Enemy.append(Enemy(Type,x,y,fliped))
        last_spawn_Time=Time

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
                if flame in group_Flame:
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
        if enemy.out_boundary:
            group_Enemy.remove(enemy)

    pygame.display.update()

def reset():
    global player, group_Enemy, group_Flame, score, Time, last_spawn_Time
    del group_Enemy[0:]
    del group_Flame[0:]
    player.reset()
    score=0
    Time=0
    last_spawn_Time=0

while True:
    clock.tick(60)

    if Time >= 120:
        start=False
        end=True

    if start and not end:
        Time=(pygame.time.get_ticks()-start_tick)//1000
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

    text_time=Font.render("TIME : "+str(Time)+" / 120",True,white)
    screen.blit(text_time,(30,30))

    text_score=Font.render("SCORE : "+str(score),True,white)
    screen.blit(text_score,(1000,30))

    text_Enemy_score=Font.render(" = 100",True,white)
    screen.blit(text_Enemy_score,(350+size_Enemy[0]*1.5,30))
    text_Enemy_score=Font.render(" = 300",True,white)
    screen.blit(text_Enemy_score,(550+size_Enemy[0]*1.5,30))
    text_Enemy_score=Font.render(" = 500",True,white)
    screen.blit(text_Enemy_score,(750+size_Enemy[0]*1.5,30))

    #show all images
    for enemy in group_Enemy:
        screen.blit(enemy.image,(enemy.pos_x,enemy.pos_y))
    for flame in group_Flame:
        screen.blit(flame.image,(flame.pos_x,flame.pos_y))
    screen.blit(player.image,(player.pos_x,player.pos_y))

    for enemy in score_Enemy:
        screen.blit(enemy.image,(enemy.pos_x,enemy.pos_y))

    if not start and not end:
        text_start=Font.render("Press Spacebar to start!", True , black)
        screen.blit(text_start,(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2-100))
    elif not start and end:
        text_end=Font.render("Game Over!",True,black)
        screen.blit(text_end,(SCREEN_WIDTH//2-80,SCREEN_HEIGHT//2-200))
        text_end2=Font.render("Score : "+str(score),True,black)
        screen.blit(text_end2,(SCREEN_WIDTH//2-80,SCREEN_HEIGHT//2-100))
        text_end3=Font.render("Press Spacebar to restart!",True,black)
        screen.blit(text_end3,(SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2))
    pygame.display.update()
