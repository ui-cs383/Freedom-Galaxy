import pygame
from loadimage import load_image

class MouseCursor(pygame.sprite.Sprite):
    def __init__(self, name):
        self.screen = pygame.display.get_surface()
        self.pos = self.screen.get_rect().center
        self.pressed = False
        self.down = False
        self.released = False
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(name, -1)
        self.rect.center = self.pos

    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.rect.midtop = self.pos
        if self.pressed:
            self.down = True
            self.rect.move_ip(-10, -10)
        if self.released:
            self.down = False
            self.pressed = False