import pygame, os
import math, random

DIR_PATH = os.path.dirname(__file__)
DIR_IMAGE = os.path.join(DIR_PATH, 'image')

#declare color
white = (255,255,255)
black = (0,0,0)
green = (51,204,0)

#declare screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
SCORE_HEIGHT = 100

#declare all size of images
size_Grass = [32,32]
size_Player = [20,20]
size_Flame = [24,24]
size_Enemy = [48,64]
size_Axe = [128,128]

################ Phase 2 Start ################
size_Experience = [16,16]
################ Phase 2 End ################


clock=pygame.time.Clock()

#class list
group_Flame = []
group_Enemy = []

################ Phase 2 Start ################
group_Experience = []
group_Axe = []
group_Garlic = []

################ Phase 2 End ################

class SpriteSheet:
    def __init__(self, filename):
        self.baseImage = pygame.image.load(os.path.join(DIR_IMAGE, filename))
        self.spr = []

    def get_image(self,x,y,size,magni):
        image = pygame.Surface(size)
        image.blit(self.baseImage, (0, 0), (x, y, size[0], size[1]))
        image_scaled = pygame.transform.scale(image,(size[0]*magni,size[1]*magni))
        image_scaled.set_colorkey(black)
        self.spr.append(image_scaled)

################ Phase 2 Start ################
class Experience(pygame.sprite.Sprite):
    def __init__(self, x, y, level):
        self.spr = SpriteSheet('Experience.png')
        for i in range(3):
            self.spr.get_image(i*size_Experience[0],0,size_Experience,2)

        self.amount = level + 1
        self.image = self.spr.spr[level]

        self.pos_x = x + size_Enemy[0] // 2
        self.pos_y = y + size_Enemy[1] // 2

        self.velocity = pygame.math.Vector2(0, 0)
        self.collected = False

    def update(self, player_pos):
        player_x = player_pos[0] + size_Player[0] // 2
        player_y = player_pos[1] + size_Player[1] // 2

        distance = math.sqrt((player_x - self.pos_x) ** 2 + (player_y - self.pos_y) ** 2)
        if distance < 80:
            acc = pygame.math.Vector2(player_x - self.pos_x, player_y - self.pos_y)
            self.velocity += acc.normalize() * 0.5

            if distance < 20:
                self.collected = True
        else:
            self.velocity *= 0.9

        self.pos_x += self.velocity.x
        self.pos_y += self.velocity.y

################ Phase 2 End ################

class Flame(pygame.sprite.Sprite):
    def __init__(self, x, y, fliped):
        self.spr = SpriteSheet('Flame-spritesheet.png')
        for i in range(7):
            self.spr.get_image(0,i*size_Flame[1],size_Flame,4)

        self.elapsedTime = 0
        self.limitTime = 1000/20

        self.pos_x=x
        self.pos_y=y

        self.fliped=fliped
        self.out_boundary=False

        self.index=0

        self.image = self.spr.spr[self.index]
        if self.fliped:
            self.image = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect(center=(self.pos_x,self.pos_y))

    def update(self):
        #check boundary
        if self.pos_x < -2*size_Flame[0] or self.pos_x > SCREEN_WIDTH:
            self.out_boundary=True
        
        #update rect
        self.rect = self.image.get_rect(center=(self.pos_x,self.pos_y))

        #update position
        if self.fliped:
            self.pos_x+=6
        else:
            self.pos_x-=6

        #show animated image
        self.elapsedTime += clock.get_time()
        if self.elapsedTime < self.limitTime:
            pass
        else:
            self.elapsedTime = 0

            self.index+=1
            if self.index >= len(self.spr.spr):
                self.index=0

            self.image=self.spr.spr[self.index]
            if self.fliped:
                self.image = pygame.transform.flip(self.image,True,False)


################ Phase 2 Start ################
class Axe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.pos_x=x + size_Player[0] // 2 - size_Axe[0] // 2
        self.pos_y=y + size_Player[1] // 2 - size_Axe[1] // 2

        self.sprite = pygame.transform.scale(
            pygame.image.load(os.path.join(DIR_IMAGE, 'Axe.png')),
            size_Axe
        )
        self.image = self.sprite
        self.rect = self.image.get_rect(center=(self.pos_x,self.pos_y))
        self.velocity = pygame.math.Vector2(random.random() * 4 - 2, -10)
        self.angle = 0

        self.out_boundary=False

    def update(self):
        #check boundary
        if self.pos_y > SCREEN_HEIGHT:
            self.out_boundary=True

        #update position
        self.velocity.y += 0.3
        self.pos_x+=self.velocity.x
        self.pos_y+=self.velocity.y
        
        #update rect
        if self.velocity.x > 0:
            self.angle -= 5
        else:
            self.angle += 5

        self.image = pygame.transform.rotate(self.sprite, self.angle)
        self.rect = self.image.get_rect(center=self.sprite.get_rect(topleft=(self.pos_x, self.pos_y)).center)

################ Phase 2 End ################


################ Phase 2 Start ################
class Garlic(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.pos_x=x + size_Player[0] // 2
        self.pos_y=y + size_Player[1] // 2

        self.range = 100
        self.image = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255, 50), (self.range, self.range), self.range)
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def update(self, player_pos):
        self.pos_x = player_pos[0] + size_Player[0] // 2
        self.pos_y = player_pos[1] + size_Player[1] // 2

        center_x = self.pos_x - self.range // 2 - size_Player[0] // 2
        center_y = self.pos_y - self.range // 2
        self.image = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255, 50), (self.range, self.range), self.range)
        self.rect = self.image.get_rect(topleft=(center_x, center_y))
        
    def is_in_range(self, enemy):
        distance = math.sqrt((self.pos_x - enemy.pos_x) ** 2 + (self.pos_y - enemy.pos_y) ** 2)
        damage_range = self.range + size_Enemy[0] // 2
        return distance < damage_range

################ Phase 2 End ################

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.elapsedTime = 0
        self.limitTime = 1000/20
        
        self.index=0
        self.spr = SpriteSheet('phoenix-cc0-spritesheet.png')

        for i in range(4):
            for j in range(5):
                self.spr.get_image(j*size_Player[0],i*size_Player[1],size_Player,4)

        self.spr_normal = [
            self.spr.spr[0],self.spr.spr[2],self.spr.spr[1],
            self.spr.spr[2],self.spr.spr[0],self.spr.spr[0],
            self.spr.spr[0],self.spr.spr[0],self.spr.spr[0]]
        self.spr_attacking = [
            self.spr.spr[5],self.spr.spr[6],self.spr.spr[7],
            self.spr.spr[8],self.spr.spr[9],self.spr.spr[10],
            self.spr.spr[11],self.spr.spr[12],self.spr.spr[13],
            self.spr.spr[14],self.spr.spr[15],self.spr.spr[16],
            self.spr.spr[17],self.spr.spr[18]]
            
        self.pos_x=SCREEN_WIDTH/2-40
        self.pos_y=SCREEN_HEIGHT/2-40

        self.attacking = False
        self.fliped = False

        self.images = self.spr_normal
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(self.pos_x,self.pos_y))

        ################ Phase 2 Start ################
        self.hp = 100

        self.level = 1
        self.exp = 0
        self.required_exp = 2

        self.tick = 0
        self.cooltime = {
            "flame": 15,
            "axe": 30 
        }

        self.upgrade_levels = [1, 0, 0, 0, 0, 0, 0, 0, 0]
        ################ Phase 2 End ################

    def flip_image(self):
        self.images=[pygame.transform.flip(image,True,False) for image in self.images]

    def reset(self):
        self.pos_x=SCREEN_WIDTH/2-40
        self.pos_y=SCREEN_HEIGHT/2-40
        self.fliped = False
        self.attacking = False
        self.images = self.spr_normal
        self.rect = self.image.get_rect(center=(self.pos_x,self.pos_y))

        ################ Phase 2 Start ################
        self.hp = 100

        self.level = 1
        self.exp = 0
        self.required_exp = 2

        self.upgrade_levels = [1, 0, 0, 0, 0, 0, 0, 0, 0]
        ################ Phase 2 End ################

    def update(self):
        #check boundary
        if self.pos_x < 0:
            self.pos_x = 0
        elif self.pos_x > SCREEN_WIDTH-size_Player[0]*4:
            self.pos_x = SCREEN_WIDTH-size_Player[0]*4
        if self.pos_y < SCORE_HEIGHT:
            self.pos_y = SCORE_HEIGHT
        elif self.pos_y > SCREEN_HEIGHT-size_Player[1]*4:
            self.pos_y = SCREEN_HEIGHT-size_Player[1]*4

        #update rect
        self.rect = self.image.get_rect(center=(self.pos_x,self.pos_y))

        #switch attacking / normal form
        if(self.attacking==True):
            self.images=self.spr_attacking
        else:
            self.images=self.spr_normal
        
        #show animated image and append flame class to group_Flame
        self.elapsedTime += clock.get_time()
        if self.elapsedTime < self.limitTime:
            pass
        else:
            self.elapsedTime = 0
            self.index+=1
            if self.index >=len(self.images):
                self.index=0
            
            # Orginal code
            # if self.attacking==True and self.index==7:
            #    group_Flame.append(Flame(self.pos_x,self.pos_y,self.fliped))
            ################ Phase 2 Start ################
            self.tick += 1
            if self.attacking==True:
                if self.tick % math.floor(self.cooltime["flame"] * (0.85 ** self.upgrade_levels[2])) == 0:
                    for i in range(self.upgrade_levels[0]):
                        gap = size_Flame[1] * 0.6
                        y = self.pos_y - gap * (self.upgrade_levels[0] - 1) + gap * i
                        group_Flame.append(Flame(self.pos_x,y,self.fliped))
                
                if self.tick % math.floor(self.cooltime["axe"] * (0.85 ** self.upgrade_levels[5])) == 0:
                    for _ in range(self.upgrade_levels[3]):
                        group_Axe.append(Axe(self.pos_x,self.pos_y))
            
            ################ Phase 2 End ################

            if(self.fliped==True):
                self.image = pygame.transform.flip(self.images[self.index],True,False)
            else:
                self.image = self.images[self.index]

class Enemy(pygame.sprite.Sprite):
    def __init__(self,Type,x,y,fliped):
        pygame.sprite.Sprite.__init__(self)

        self.elapsedTime = 0
        self.limitTime = 1000/8
        
        #set enemy type information : Type 1(blue), 2(yellow), 3(violet)
        self.Type = Type
        self.health = 0
        self.velocity = 0.0
        self.score = 0
        self.out_boundary = False
        y_index = 0
        if self.Type == 1:
            self.health = 1
            self.velocity = 1.5
            self.score=100
            y_index=0
        elif self.Type == 2:
            self.health = 2
            self.velocity = 3
            self.score=300
            y_index = 2
        elif self.Type == 3:
            self.health = 3
            self.velocity = 1
            self.score = 500
            y_index = 4

        self.index = 0
        self.spr = SpriteSheet('Slime2.png')
        for i in range(4):
            self.spr.get_image(67+64*i,73+64*y_index,size_Enemy,1.5)

        ################ Phase 2 Start ################
        self.hit_spr = SpriteSheet('Slime2.png')
        for i in range(4):
            self.hit_spr.get_image(67+64*i,73+64*11,size_Enemy,1.5)

        self.hit_tick = 0
        ################ Phase 2 End ################

        self.pos_x = x
        self.pos_y = y
        self.fliped = fliped

        self.images = self.spr.spr
        self.image = self.spr.spr[0]
        self.rect = self.image.get_rect(center=(self.pos_x,self.pos_y))

        ################ Phase 2 Start ################
        self.chase = random.choice([True, False])
        ################ Phase 2 End ################

    def update(self, player_pos):
        #update position
        ################ Phase 2 Start ################
        if self.chase:
            if player_pos[0] > self.pos_x:
                self.pos_x += self.velocity
            elif player_pos[0] < self.pos_x:
                self.pos_x -= self.velocity
            if player_pos[1] > self.pos_y:
                self.pos_y += self.velocity
            elif player_pos[1] < self.pos_y:
                self.pos_y -= self.velocity
        ################ Phase 2 End ################
        else:
            f=1
            if self.fliped:
                f=-1
            if self.index%2==1:
                self.pos_x+=self.velocity*f
            else:
                self.pos_x+=1*f

        #check out_boundary
        if self.pos_x<-100 or self.pos_x>SCREEN_WIDTH+100:
            self.out_boundary=True

        #update rect
        self.rect = self.image.get_rect(center=(self.pos_x,self.pos_y))

        #show animated image
        self.elapsedTime += clock.get_time()
        if self.elapsedTime < self.limitTime:
            pass
        else:
            self.elapsedTime = 0
            
            self.index+=1
            if self.index >=len(self.images):
                self.index=0
            
            self.image = self.images[self.index]

            ################ Phase 2 Start ################
            if self.hit_tick > 0:
                self.hit_tick -= 1
                self.image = self.hit_spr.spr[self.index]
            ################ Phase 2 End ################


################ Phase 2 Start ################
class Upgrade(pygame.sprite.Sprite):
    def __init__(self, type, level):
        self.type = type

        self.weapon_type = self.type // 3
        self.upgrade_type = self.type % 3

        self.spr = SpriteSheet('Upgrade.png')
        for i in range(3):
            self.spr.get_image(1024*i, 0, (1024, 1024), 0.08)
        self.image = self.spr.spr[self.weapon_type]

        self.value = [level, 1.15 ** level, 0.85 ** level][self.upgrade_type]
        if self.upgrade_type == 0:
            self.description = f"Increase projectile to {self.value}"
        elif self.upgrade_type == 1:
            self.description = f"Increase damage by {self.value:.2f} times"
        elif self.upgrade_type == 2:
            self.description = f"Decrease cooldown by {self.value:.2f} times"
################ Phase 2 End ################