#!usr/bin/python

import pygame, Buttons
import pygame.font
from pygame.locals import *
import Queue
import thread
import time

GREEN = (0, 255, 0)
LIGHT_BLUE = (30,144,255)
WHITE = (255,255,255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

BUTTON_TEXT = "Log"

pygame.init()


#Based on example from http://www.pygame.org/pcr/text_rect/index.php
# This class will automatically wrap text within a rectangle
def render_textrect(string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    import pygame
    
    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size) 
    surface.fill(background_color) 

    accumulated_height = 0 
    for line in final_lines: 
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException, "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]

    return surface

class Button:
    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x,y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length//len(text))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):           
        for i in range(1,10):
            s = pygame.Surface((length+(i*2),height+(i*2)))
            s.fill(color)
            alpha = (255/(i+2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x-i,y-i,length+i,height+i), width)
            surface.blit(s, (x-i,y-i))
        pygame.draw.rect(surface, color, (x,y,length,height), 0)
        pygame.draw.rect(surface, (190,190,190), (x,y,length,height), 1)  
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        print "Some button was pressed!"
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False


class Log_Button:

    def __init__(self, queue):
        self.queue = queue
        self.main()
    
    #Create a display
    def display(self):
        self.screen = pygame.display.set_mode((800,600))  #Set window display resolution
        pygame.display.set_caption("Log menu test")
        
    #Update the display and show the button
    def update_display(self, LogFlag):
        #self.screen.fill(LIGHT_BLUE)
        self.LogFlag = LogFlag
        #Parameters:               surface,     color, x,   y,   length, height, width, text,       text_color
        #self.Button1.create_button(self.screen, GREEN, 10,  550,    100,    30,   0,    BUTTON_TEXT, WHITE)
        pygame.display.flip()
        
        if(LogFlag == True):
            #If LogFlag is set, then display the text window
            #Curr_Cnt = self.queue.get()
            #Format the output string
            MY_STRING = "This is a test string"
            my_font = pygame.font.Font(None, 22)
            my_rect = pygame.Rect((0, 450, 200, 150))
            Log_Window = pygame.Rect((40, 40, 300, 300))
            rendered_text = render_textrect(MY_STRING, my_font, my_rect, (216, 216, 216), (48, 48, 48), 0)
            self.screen.blit(rendered_text, my_rect.topleft)
            #Add a close button to the log
            #Parameters:                      surface,    color, x,   y,   length, height, width, text,       text_color
            self.CloseLogButton.create_button(self.screen, RED, 180,  460,    10,    10,   10,    "X", BLACK)
        else:
            #Else, fill over the text window
            self.screen.fill(LIGHT_BLUE)
            self.LogButton.create_button(self.screen, GREEN, 10,  550,    100,    30,   0,    BUTTON_TEXT, WHITE)

    
    #Run the loop
    def main(self):
        LogFlag = False
        self.LogButton = Buttons.Button()
        self.CloseLogButton = Buttons.Button()
        self.display()
        self.screen.fill(LIGHT_BLUE)
        while True:
            self.update_display(LogFlag)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    #If the Log button is pressed, then display the window
                    #Change to be based off of mouse position
                    if self.LogButton.pressed(pygame.mouse.get_pos()):
                        #print "- Displaying Log"
                        #print self.queue.get()
                        LogFlag = True
                    elif self.CloseLogButton.pressed(pygame.mouse.get_pos()):
                        #print "- Closing Log"
                        LogFlag = False
                        
                        
#Threaded Counting function for demonstration log output
def Counting():
    cnt = 0
    while True:
        cnt += 1
        queue.put(cnt)
        
        
            
        
if __name__ == '__main__':
    queue = Queue.Queue()
    thread.start_new_thread(Counting, ())
    obj = Log_Button(queue)
    
    
