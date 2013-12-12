#@PydevCodeAnalysisIgnore
#Planetary Menu Bar Class
#Paul Bailey

import pygame, sys, os
from support.loadimage import load_image
from pygame.locals import *

pygame.init()
'''
#The load_image method should be an import in the final version, it is included explicitly for test purposes
def load_image(image, colorkey=None):
    path = os.path.join('Data', image)
    print path
    try:
        image = pygame.image.load(path)
    except pygame.error, message:
        print 'Can not load image:', image
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image, image.get_rect()
'''
blackcolor = (0,0,0)
whitecolor = (255,255,255)
redcolor = (243,14,14)
lightbluecolor = (100,149,237)

#Marks the position of the Menu Bar relative to the master background screen
MenuBarUpperLeftCorner = (90,0) # For test purposes. The final product will pass these coordinates into the initialization
x = MenuBarUpperLeftCorner[0] # take out
y = MenuBarUpperLeftCorner[1] #take out

#Planet Names for testing purposes
planetname = "NameofPlanet" 
planet1name = "Quibron"
planet2name = "Angoff"
planet3name = "Charkhan"
planet4name = "planet1"
planet5name = "planet2"

#planet
planetposition = (600, 70) #(x+510, y+70)
planettextcolor = (0,0,0)
planetnameposition = (x+445,y+100)

#pdb box
pdbupcolor = (52, 243, 14) # not used
pdbdowncolor = redcolor
pdbbox = (x+10,y+30,100,100)
pdbboxpostion = (x+10,y+30)
pdbstatustextcolor = (34,34,34)
pdbstatustextposition = (x+17,y+5)
pdbdowntext = "PDB Down"
pdbdowntextcolor = (0,0,0)
pdbdowntextpostition = (x+16,y+70)
pdbdowntextrect = pygame.font.Font(None, 25)
pdbdowntextsurface = pdbdowntextrect.render(pdbdowntext,1,pdbdowntextcolor)

#Rebellion Status
rebellionstatustext = "Rebellion Status"
rebellionstatusrect = pygame.font.Font(None, 20)
rebellionstatussurface = rebellionstatusrect.render(rebellionstatustext,1,whitecolor)
rebellionstatusposition = (x+150,y+5)

#Rebellion Box
inrebelliontext = "In Rebellion"
norebelliontext = "No Rebellion"
rebellionboxposition = (x+150,y+30)
rebellionboxsize = (115,30)
rebellionboxrect = pygame.Rect(rebellionboxposition,rebellionboxsize)

rebelliontextposition = (x+155,y+35)

inrebelliontextrect = pygame.font.Font(None,25)
inrebelliontextsurface = inrebelliontextrect.render(inrebelliontext,1,blackcolor)

norebelliontextrect = pygame.font.Font(None,25)
norebelliontextsurface = norebelliontextrect.render(norebelliontext,1,blackcolor)

#Control Box
controlstatustext = "Control  Status"
controlstatusrect = pygame.font.Font(None,20)
controlstatussurface = controlstatusrect.render(controlstatustext,1,whitecolor)
controlstatusposition = (x+150,y+80)

imperialtext = "Imperial"
rebeltext = "Rebel"
controlboxposition = (x+150,y+100)
controlboxsize = (115,30)
controlboxrect = pygame.Rect(controlboxposition,controlboxsize)

controltextposition = (x+175,y+105)

imperialtextrect = pygame.font.Font(None,25)
imperialtextsurface = imperialtextrect.render(imperialtext,1,blackcolor)

rebeltextrect = pygame.font.Font(None,25)
rebeltextsurface = rebeltextrect.render(rebeltext,1,blackcolor)


#System and Planet Title
planetsystemtext = "System                         Planet"
planetsystemrect = pygame.font.Font(None, 25)
planetsystemsurface = planetsystemrect.render(planetsystemtext,1,whitecolor)
planetsystemposition = (x+310,y+78)


#Menu Bar
backgroundcolor = (100,150,200) 
menubarcolor = (146,149,145)
menubarposandsize = (x, y, 620, 150)

#loyalty box
loyaltybox = (x+300, y+22, 300, 50)
loyaltycolor = (255,255,255)
loyaltytext = "Patriotic   Loyal   Neutral   Dissent   Unrest"
loyaltytextboxposition = (x+300,y+5,100,100)
loyaltytextcolor = (50,50,50)
loyaltyposition1 = (x+325,y+35)
loyaltyposition2 = (x+380,y+35)
loyaltyposition3 = (x+435,y+35)
loyaltyposition4 = (x+500,y+35)
loyaltyposition5 = (x+560,y+35)
loyaltymarkercolor = (0,0,0)
loyaltymarkersize = (25,25)
loyaltymarker5 = pygame.Rect(loyaltyposition5, loyaltymarkersize)

#system
systemname = "Egrix"
systemnametextcolor = blackcolor
systemnametextposition = (x+300,y+100)
systemnametextrect = pygame.font.Font(None, 50)
systemnametextsurface = systemnametextrect.render(systemname,1,systemnametextcolor)

#Test Screen
screensize = (800,600)
screen = pygame.display.set_mode(screensize)
starbg = pygame.image.load("data/stars.jpg")
starbg = pygame.transform.scale(starbg, (screensize))

#menubar    
menubar = pygame.Rect(menubarposandsize)

#loyalty
loyaltyrect = pygame.Rect(loyaltybox)
loyaltytextrect = pygame.Rect(loyaltytextboxposition)
loyaltymarker1 = pygame.Rect(loyaltyposition1, loyaltymarkersize)
loyaltymarker2 = pygame.Rect(loyaltyposition2, loyaltymarkersize)
loyaltymarker3 = pygame.Rect(loyaltyposition3, loyaltymarkersize)
loyaltymarker4 = pygame.Rect(loyaltyposition4, loyaltymarkersize)

PlanetName = pygame.font.Font(None, 50)
pdbtextrect = pygame.font.Font(None, 25)
loyaltytextrectfont = pygame.font.Font(None, 20)
      
planetname = planet1name
pdbstatustext = "PDB Status"
pdbstatustextrect = pygame.font.Font(None, 20)

pdbfontsurface = pdbtextrect.render(pdbstatustext, 1, (255,255,255))
planetFontSurface = PlanetName.render(planetname, 1, planettextcolor)
loayaltytextsurface = loyaltytextrectfont.render(loyaltytext, 1, loyaltytextcolor)
pdbstatustexsurface = pdbstatustextrect.render(pdbstatustext, 1, (255,255,255))

pdbdownrect = pygame.Rect(pdbbox)
pdb_image, pdbrect = load_image("pdbup.png", None)
pdbrect.topleft = pdbboxpostion



class MenuBar():
    def __init__(self, planetname, loyaltystate, backgroundcolor, pdbup, position):#, PDBstatus=None):
        self.planetname = planetname
        #self.planetnametextcolor = planetnametextcolor
        self.loyaltystate = loyaltystate
        self.pdbup = pdbup
        self.pdbcontrol = "Rebel"
        self.backgroundcolor = backgroundcolor
        self.planetboxcolor = (255,200,200)
        self.buttoncolor = (50,102,255)
        self.position = position
        self.rebellionstatus = False
        self.rebelcontrolstatus = True
        
    def draw(self, screen, menubar):
        pygame.draw.rect(screen, menubarcolor, menubar, 0)
        pygame.draw.rect(screen, loyaltycolor, loyaltyrect, 0)
        pygame.transform.scale(starbg, (screensize))
        screen.blit(planetFontSurface, planetnameposition) #planetname position
        screen.blit(pdbfontsurface,pdbboxpostion)
        screen.blit(loayaltytextsurface, loyaltytextboxposition)
        screen.blit(pdbstatustexsurface, pdbstatustextposition)
        screen.blit(systemnametextsurface, systemnametextposition)
        screen.blit(planetsystemsurface, planetsystemposition)
        screen.blit(rebellionstatussurface, rebellionstatusposition)
        screen.blit(controlstatussurface,controlstatusposition)
        if self.rebelcontrolstatus == True:
            pygame.draw.rect(screen,redcolor,controlboxrect,0)
            screen.blit(rebeltextsurface,controltextposition)
        else:
            pygame.draw.rect(screen,lightbluecolor,controlboxrect,0)
            screen.blit(imperialtextsurface,controltextposition)
        
        if self.rebellionstatus == True:
            pygame.draw.rect(screen,redcolor,rebellionboxrect,0)
            screen.blit(inrebelliontextsurface,rebelliontextposition)
        else:
            pygame.draw.rect(screen,lightbluecolor,rebellionboxrect,0)
            screen.blit(norebelliontextsurface,rebelliontextposition)
        if self.pdbup == True:
            screen.blit(pdb_image, pdbboxpostion)
        else:
            pygame.draw.rect(screen, pdbdowncolor, pdbdownrect, 0)
            screen.blit(pdbdowntextsurface, pdbdowntextpostition)
        if self.loyaltystate == 1:
            pygame.draw.rect(screen, loyaltymarkercolor, loyaltymarker1, 0)
        elif self.loyaltystate == 2:
            pygame.draw.rect(screen, loyaltymarkercolor, loyaltymarker2, 0)            
        elif self.loyaltystate == 3:
            pygame.draw.rect(screen, loyaltymarkercolor, loyaltymarker3, 0)            
        elif self.loyaltystate == 4:
            pygame.draw.rect(screen, loyaltymarkercolor, loyaltymarker4, 0)            
        elif self.loyaltystate == 5:
            pygame.draw.rect(screen, loyaltymarkercolor, loyaltymarker5, 0)            
            
        
    def update(self, planetname, loyaltystate, pdbup, systemname, rebellionstatus, rebelcontrolstatus):
        self.planetname = planetname
        self.loyaltystate = loyaltystate
        self.pdbup = pdbup
        self.systemname = systemname
        self.rebellionstatus = rebellionstatus
        self.rebelcontrolstatus = rebelcontrolstatus
        
if __name__ == '__main__':




    menu = MenuBar(planet1name, 1, backgroundcolor, True, (90,0) )   
    
    while 1:
        #refresh process
        #do updating
        #draw proccess


#This section was made to test various states of the planetary menu class
        screen.blit(starbg, (0,0))
        menu.draw(screen, menubar)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and menu.planetname == planet1name:
                menu.update(planet2name, 3, True, "Shiny Star",False,False)
                planetFontSurface = PlanetName.render(menu.planetname, 1, planettextcolor)
            elif event.type == pygame.MOUSEBUTTONDOWN and menu.planetname == planet2name:
                menu.update(planet3name, 4, False, "Shiny Star",True,True)
                planetFontSurface = PlanetName.render(menu.planetname, 1, planettextcolor)
            elif event.type == pygame.MOUSEBUTTONDOWN and menu.planetname == planet3name:
                menu.update(planet4name, 5, True, "Shiny Star",False,False)
                planetFontSurface = PlanetName.render(menu.planetname, 1, planettextcolor)
            elif event.type == pygame.MOUSEBUTTONDOWN and menu.planetname == planet4name:
                menu.update(planet5name, 1, True, "Shiny Star",True,True)
                planetFontSurface = PlanetName.render(menu.planetname, 1, planettextcolor)
            elif event.type == pygame.MOUSEBUTTONDOWN and menu.planetname == planet5name:
                menu.update(planet1name, 2, True, "Shiny Star",False,False)
                planetFontSurface = PlanetName.render(menu.planetname, 1, planettextcolor)
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()        















