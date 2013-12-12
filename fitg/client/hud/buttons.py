#Joe Matranga

import pygame


class Button():
    def __init__(self):
        self.flag = False
        self.rect = pygame.Rect

    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x, y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length // (len(text) * 0.7))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 3, text_color)
        surface.blit(myText, ((x + length / 2) - myText.get_width() / 2, (y + height / 2) - myText.get_height() / 2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):
        #for i in range(1,10):
        s = pygame.Surface((length, height))
        s.fill(color)
        #alpha = (255/(i+2))
        #if alpha <= 0:
        #    alpha = 1
        #s.set_alpha(alpha)
        pygame.draw.rect(s, color, (x, y, length, height), width)
        #surface.blit(s, (x-i,y-i))
        pygame.draw.rect(surface, color, (x, y, length, height), 0)
        #pygame.draw.rect(surface, (190,190,190), (x,y,length,height), 1)
        return surface

    def pressed(self, mouse_cursor):
        #print "The mouse cursor is a :"+str(type(mouse_cursor))
        if self.rect.colliderect(mouse_cursor):
            return True
        else:
            return False


class TextRectException():
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message


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
                    raise TextRectException  # "The word " + word + " is too long to fit in the rect passed."
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
        #if accumulated_height + font.size(line)[1] >= rect.height:
            #raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException  # "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]

    return surface



#Draw menus and buttons based off of flag values


class Menu():
    def __init__(self, screen):
        self.Log_Stack = []
        self.Log_Button = Button()
        self.Close_Log_Button = Button()
        self.Search_Button = Button()
        self.Combat_Button = Button()
        self.Mission_Button = Button()
        #self.HelpButton = Button()
        #self.CloseHelpButton = Button()
        #Initialize the hidden buttons
        self.Close_Log_Button.create_button(screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
        
    def draw_buttons(self, screen, height, width, selected_unit):
        detail_width = width*0.325
        detail_height = height*0.85
        details_rect = pygame.Rect((detail_width, detail_height, width*0.35, height*0.2))
        rect_11 = pygame.Rect((detail_width, detail_height, 50, 50))
        rect_12 = pygame.Rect(((detail_width)+50, detail_height, 50, 50))
        rect_13 = pygame.Rect(((detail_width)+100, detail_height, 50, 50))
        rect_14 = pygame.Rect(((detail_width)+150, detail_height, 50, 50))
        rect_21 = pygame.Rect((detail_width, (detail_height)+50, 50, 50))
        rect_22 = pygame.Rect(((detail_width)+50, (detail_height)+50, 50, 50))
        rect_23 = pygame.Rect(((detail_width)+50, (detail_height)+50, 50, 50))
        rect_24 = pygame.Rect(((detail_width)+50, (detail_height)+50, 50, 50))
        prev_unit = None
        LIGHT_GREY = (82,82,82)
        if(self.Log_Button.flag == True):
            #If LogFlag is set, then display the text window
            #Format the output string
            if(len(self.Log_Stack) > 10):
                self.Log_Stack.pop()
            Log_Message = ""
            for item in self.Log_Stack:
                Log_Message = Log_Message + str(item) + "\n"
            log_font = pygame.font.Font(None, 15)
            log_rect = pygame.Rect((0, height * 0.82, width*0.29, height*0.18))
            rendered_text = render_textrect(Log_Message, log_font, log_rect, (216, 216, 216), (48, 48, 48), 0)
            screen.blit(rendered_text, log_rect.topleft)
            #Parameters:                 surface, color,       x,             y,       length, height, width, text,  text_color
            self.Close_Log_Button.create_button(screen, (255, 0, 0), width*0.28,  height*0.82,    10,    10,   10,    "X", (0, 0, 0))
        else:
            self.Log_Button.create_button(screen, LIGHT_GREY, width*0.01,  height*0.96,  width*0.097,  height*0.038,   0,  "Log   ", (255, 255, 255))
            
        self.Search_Button.create_button(screen, LIGHT_GREY, width*0.879,  height*0.86, width*0.1, height*0.04, 0, "Search", (255, 255, 255))
        self.Combat_Button.create_button(screen, LIGHT_GREY, width*0.879,  height*0.91, width*0.1, height*0.04, 0, "Combat", (255, 255, 255))
        self.Mission_Button.create_button(screen, LIGHT_GREY, width*0.879,  height*0.96, width*0.1, height*0.04, 0, "Mission", (255, 255, 255))
        pygame.draw.rect(screen, (48, 48, 48), details_rect)
        #Help Button and menu
        #    if(self.HelpButton.flag == True):
        #        Help_Message = "This text will change based on the current player phase"
        #        help_bg = pygame.Rect((0, 0, width*0.292, height*0.38))
        #        pygame.draw.rect(screen, (48, 48, 48), help_bg)
        #        help_font = pygame.font.Font(None, 15)
        #        help_rect = pygame.Rect((0, height*0.025, width*0.292, height*0.35))
        #        rendered_text = render_textrect(Help_Message, help_font, help_rect, (216, 216, 216), (48, 48, 48), 0)
        #        screen.blit(rendered_text, help_rect.topleft)
        #        #Parameters:                 surface, color,       x,            y,            length, height, width, text,  text_color
        #        CloseHelpButton.create_button(screen, (255, 0, 0), width*0.278,  height*0.006,    10,    10,   10,    "X", (0, 0, 0))
        #    else:
        #        HelpButton.create_button(screen, LIGHT_GREY, width*0.005,  height*0.006,  width*0.097,  height*0.038,   0,  "Help  ", (255, 255, 255))
        if (selected_unit):
            if (prev_unit != selected_unit):
                prev_unit = selected_unit
        
        i = 0
        if (prev_unit):
            for unit in selected_unit.stack_list:
                if (i == 0):
                    screen.blit(unit.image, rect_11)
                    break;
                elif (i == 1):
                    screen.blit(unit.image, rect_12)
                    break;
                elif (i == 2):
                    screen.blit(unit.image, rect_13)
                    break;
                elif (i == 3):
                    screen.blit(unit.image, rect_14)
                    break;
                elif (i == 4):
                    screen.blit(unit.image, rect_21)
                    break;
                elif (i == 5):
                    screen.blit(unit.image, rect_22)
                    break;
                elif (i == 6):
                    screen.blit(unit.image, rect_23)
                    break;
                elif (i == 7):
                    screen.blit(unit.image, rect_24) 
                    break;
                else:
                    print "ERROR: Too many units to display"
     
                i += 1
        

    def update_buttons(self, mouse_cursor):
    
        #If the Log button is pressed, then display the window
        if self.Log_Button.pressed(mouse_cursor):
            self.Log_Button.flag = True
        elif self.Close_Log_Button.pressed(mouse_cursor):
            self.Log_Button.flag = False
        elif self.Search_Button.pressed(mouse_cursor):
            self.Search_Button.flag = True
            #Bring up Search Menu
        elif self.Combat_Button.pressed(mouse_cursor):
            self.Combat_Button.flag = True
            #Bring up Combat Menu
        elif self.Mission_Button.pressed(mouse_cursor):
            self.Mission_Button.flag = True
            #Bring up Mission Menu
