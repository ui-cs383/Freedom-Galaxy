import os
import sys
import pygame

def load_image(image, colorkey=None):
    path = os.path.join('data', image)
    #print path
    try:
        image = pygame.image.load(path)
    except pygame.error, message:
        print 'Can not load image:', image
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)  # pygame.RLEACCEL can improve performance
    else:
        image = image.convert_alpha()
    return image, image.get_rect()