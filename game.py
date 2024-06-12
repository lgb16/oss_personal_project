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

############### Phase 2 Start ################
upgrading = False
upgrade_choice = 0
upgrade_options = ["Flame", "Axe", "Garlic"]
upgrade_key_pressed = False

def select_upgrade():
    global upgrading, upgrade_choice, upgrade_options, upgrade_key_pressed

    key_event = pygame.key.get_pressed()
    if not upgrade_key_pressed:
        if key_event[pygame.K_UP]:
            upgrade_choice = max(0, upgrade_choice - 1)
            upgrade_key_pressed = True
        if key_event[pygame.K_DOWN]:
            upgrade_choice = min(2, upgrade_choice + 1)
            upgrade_key_pressed = True
    else:
        if not key_event[pygame.K_UP] and not key_event[pygame.K_DOWN]:
            upgrade_key_pressed = False

    if key_event[pygame.K_a]:
        print(upgrade_choice)
        upgrading = False

def draw_upgrade(screen):
    card_height = 100
    card_width = 300
    card_gap = 20

    card_y = (SCREEN_HEIGHT - (card_height * 3 + card_gap * 2)) // 2
    for i, option in enumerate(upgrade_options):
        x = (SCREEN_WIDTH - card_width) // 2
        y = card_y + (i * (card_height + card_gap))

        if i == upgrade_choice:
            pygame.draw.rect(screen, white, pygame.Rect(x, y, card_width, card_height))
            pygame.draw.rect(screen, black, pygame.Rect(x + 4, y + 4, card_width - 8, card_height - 8))
        else:
            pygame.draw.rect(screen, black, pygame.Rect(x, y, card_width, card_height))

        font = pygame.font.Font(None, 24)
        text_surface = font.render(option, True, white)
        screen.blit(text_surface, (x, y))
################ Phase 2 End ################


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
            ############### Phase 2 Start ################
            player.hp -= 1
            if player.hp <= 0:
            ################ Phase 2 End ################
                global start, end
                start=False
                end=True

    #check collide flame and ememy
    for flame in group_Flame:
        for enemy in group_Enemy:
            if pygame.sprite.collide_mask(flame, enemy):
                enemy.health-=1
                enemy.hit_tick = 3
                if flame in group_Flame:
                    group_Flame.remove(flame)

    ################ Phase 2 Start ################
    for axe in group_Axe:
        for enemy in group_Enemy:
            if pygame.sprite.collide_mask(axe, enemy):
                enemy.health -= 0.2
                enemy.hit_tick = 3
    ################ Phase 2 End ################

    ################ Phase 2 Start ################
    if len(group_Garlic) == 0:
        group_Garlic.append(Garlic(player.pos_x, player.pos_y))

    garlic = group_Garlic[0]
    for enemy in group_Enemy:
        if garlic.is_in_range(enemy):
            enemy.health -= 0.1
            enemy.hit_tick = 3

    ################ Phase 2 End ################

    ################ Phase 2 Start ################
    global score
    for enemy in group_Enemy:
        if enemy.health <= 0:
            score += enemy.score
            group_Enemy.remove(enemy)

            level = enemy.Type - 1
            group_Experience.append(Experience(enemy.pos_x, enemy.pos_y, level))
    
    ################ Phase 2 End ################

    #update all classes
    for flame in group_Flame:
        flame.update()
        if flame.out_boundary:
            group_Flame.remove(flame)
    player.update()
    for enemy in group_Enemy:
        # enemy.update()
        ################ Phase 2 Start ################
        enemy.update((player.pos_x, player.pos_y))
        ################ Phase 2 End ################
        if enemy.out_boundary:
            group_Enemy.remove(enemy)

    ################ Phase 2 Start ################
    for exp in group_Experience:
        exp.update((player.pos_x, player.pos_y))
        if exp.collected:
            player.exp += exp.amount
            group_Experience.remove(exp)

            if player.exp >= player.required_exp:
                player.level += 1
                player.exp = player.exp % player.required_exp
                player.required_exp += 10

                global upgrading
                upgrading = True

    for axe in group_Axe:
        axe.update()
        if axe.out_boundary:
            group_Axe.remove(axe)

    for garlic in group_Garlic:
        garlic.update((player.pos_x, player.pos_y))
    ################ Phase 2 End ################


    pygame.display.update()

def reset():
    global player, group_Enemy, group_Flame, score, Time, last_spawn_Time
    ################ Phase 2 Start ################
    global group_Experience, group_Axe, group_Garlic
    del group_Experience[0:]
    del group_Axe[0:]
    del group_Garlic[0:]
    ################ Phase 2 End ################

    del group_Enemy[0:]
    del group_Flame[0:]
    player.reset()
    score=0
    Time=0
    last_spawn_Time=0


while True:
    ############### Phase 2 Start ################
    if upgrading:
        select_upgrade()
    else:
    ################ Phase 2 End ################
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

    ################ Phase 2 Start ################
    for exp in group_Experience:
        screen.blit(exp.image, (exp.pos_x, exp.pos_y))

    for axe in group_Axe:
        screen.blit(axe.image, axe.rect.topleft)

    for garlic in group_Garlic:
        screen.blit(garlic.image, garlic.rect.topleft)
    ################ Phase 2 End ################

    ################ Phase 2 Start ################
    red = (255, 0, 0)
    green = (0, 255, 0)
    bar_width = 64
    bar_height = 10

    center_x, center_y = player.rect.center
    bar_x = center_x - bar_width // 2 + 44
    bar_y = center_y + 85
    hp = player.hp

    green_bar_width = (player.hp / 100) * bar_width
    pygame.draw.rect(screen, red, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, green, (bar_x, bar_y, green_bar_width, bar_height))
    ################ Phase 2 End ################

    ################ Phase 2 Start ################
    blue = (0, 0, 255)
    bar_width = SCREEN_WIDTH
    bar_height = 20

    bar_x = 0
    bar_y = SCORE_HEIGHT - bar_height

    blue_bar_width = (player.exp / player.required_exp) * bar_width
    pygame.draw.rect(screen, black, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, blue, (bar_x, bar_y, blue_bar_width, bar_height))

    font = pygame.font.Font(None, 24)
    text = font.render("LV " + str(player.level), True, white)
    screen.blit(text, (bar_x + 10, bar_y + 4))
    ################ Phase 2 End ################

    ################ Phase 2 Start ################
    if upgrading:
        draw_upgrade(screen)
    ################ Phase 2 End ################

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
