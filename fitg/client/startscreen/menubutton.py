import pygame

class my_button:
    def __init__(self, text, alttext='', fontsize = 40):
        self.text = text
        self.alttext = alttext
        self.is_alt = False
        self.is_hover = False
        self.fontsize = fontsize
        self.default_color = (100,100,100)
        self.hover_color = (204,102, 0)
        self.font_color = (220, 220, 20)
        self.obj = None
        
    def switch_text(self):
        self.is_alt = not self.is_alt
        
    def label(self):
        font = pygame.font.Font(None, self.fontsize)
        if self.is_alt:
            return font.render(self.alttext, 1, self.font_color)
        else:
            return font.render(self.text, 1, self.font_color)
        
    def color(self):
        if self.is_hover:
            return self.hover_color
        else:
            return self.default_color
            
    def draw(self, screen, mouse, rect_coord, label_coord):
        self.obj  = pygame.draw.rect(screen, self.color(), rect_coord)
        screen.blit(self.label(), label_coord)
        self.check_hover(mouse)
        
    def check_hover(self, mouse):
        if self.obj.collidepoint(mouse):
            self.is_hover = True 
        else:
            self.is_hover = False