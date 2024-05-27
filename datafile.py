import pygame, os

DIR_PATH = os.path.dirname(__file__)
DIR_IMAGE = os.path.join(DIR_PATH, 'image')

white = (255,255,255)
black = (0,0,0)

class SpriteSheet:
    def __init__(self, filename, width, height, max_row, max_col, max_index):
        baseImage = pygame.image.load(os.path.join(DIR_IMAGE, filename))
        self.spr = []

        for i in range(max_index):
            image = pygame.Surface((width, height))
            image.blit(baseImage, (0, 0),
                    ((i%width)*width, (i//max_row)*height, width, height))
            image_scaled = pygame.transform.scale(image,(width*4,height*4))
            #for frame in image:
            #    frame.set_colorkey(BLACK)
            image_scaled.set_colorkey(black)
            self.spr.append(image_scaled)
