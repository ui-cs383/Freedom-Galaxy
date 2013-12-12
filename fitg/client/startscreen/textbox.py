import pygame

class my_textbox:
    def __init__(self, title):
        self.title = title
        self.text = []
        self.input = ''
        self.default_color = (100,100,100)
        self.font_color = (220, 220, 20)
        self.obj = None
        self.nextchar = "_"
    
    def switchchar (self):
        if self.nextchar == "_":
            self.nextchar = chr(9)
        else:
            self.nextchar ="_"
        
    def label(self, text):
        font = pygame.font.Font(None, 20)
        return font.render(text, 1, self.font_color)
        
    def addkey (self, inkey):
        if inkey == pygame.K_BACKSPACE:
            self.text = self.text[0:-1]
        elif inkey == pygame.K_MINUS:
            self.text.append("-")
        elif inkey <= 127:
            if len(self.text) < 30:
                self.text.append(chr(inkey))
        self.input = ''
        self.input = self.input.join(self.text)
    
    def draw (self, screen, rect_coord):
        label_coord = (rect_coord[0]+4, rect_coord[1]+4)
        self.obj = pygame.draw.rect(screen, self.default_color, rect_coord)
        screen.blit(self.label(self.title), (label_coord[0], label_coord[1]))
        screen.blit(self.label(self.input+self.nextchar), (label_coord[0], label_coord[1]+20))
        pygame.draw.line(screen, self.font_color, (label_coord[0], label_coord[1]+33),(label_coord[0]+242, label_coord[1]+33))