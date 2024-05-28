import pygame, os

DIR_PATH = os.path.dirname(__file__)
DIR_IMAGE = os.path.join(DIR_PATH, 'image')

#declare color
white = (255,255,255)
black = (0,0,0)

#declare screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

clock=pygame.time.Clock()

class SpriteSheet:
    def __init__(self, filename, width, height, max_row, max_col, max_index):
        baseImage = pygame.image.load(os.path.join(DIR_IMAGE, filename))
        self.spr = []

        for i in range(max_index):
            image = pygame.Surface((width, height))
            image.blit(baseImage, (0, 0),
                    ((i%max_row)*width, (i//max_row)*height, width, height))
            image_scaled = pygame.transform.scale(image,(width*4,height*4))
            image_scaled.set_colorkey(black)
            self.spr.append(image_scaled)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.elapsedTime = 0
        self.limitTime = 1000/20
        
        self.index=0
        self.spr = SpriteSheet('phoenix-cc0-spritesheet.png',20,20,5,4,19)
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

    def flip_image(self):
        self.images=[pygame.transform.flip(image,True,False) for image in self.images]

    def update(self):
        if(self.attacking==True):
            self.images=self.spr_attacking
        else:
            self.images=self.spr_normal

        self.elapsedTime += clock.get_time()
        if self.elapsedTime < self.limitTime:
            pass
        else:
            self.elapsedTime = 0
            self.index+=1
            if self.index >=len(self.images):
                self.index=0
            if(self.fliped==True):
                self.image = pygame.transform.flip(self.images[self.index],True,False)
            else:
                self.image = self.images[self.index]
