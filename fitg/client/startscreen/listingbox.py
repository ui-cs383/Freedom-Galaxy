import pygame
from menubutton import my_button

class gamelistingbox:
    def __init__ (self):
        self.obj = None
        self.default_color = (50,50,50)
        self.hover_color = (204,102, 0)
        self.font_color = (220, 220, 20)
        self.fontsize = 20
        self.joinbutton = my_button("Join", fontsize = self.fontsize)
        self.cancelbutton = my_button("Cancel", fontsize = self.fontsize)
        self.refreshbutton = my_button("Refresh", fontsize = self.fontsize)
        self.visible = False
        self.scenarioflag = False
        self.x = 30
        self.y = 275
        self.width = 475
        self.height = 250
        self.selectedgame = None
        self.selectedindex = None
        self.gamelist = []
        self.namelist = []
        self.playerlist = []
        self.scenariolist = []
        self.sidelist = []
        self.gamebox = pygame.Rect(self.x, self.y+self.fontsize, self.width, self.fontsize*len(self.namelist))
        self.loadingtext = self.label("Loading", 60)
        
    def label(self, text, font_size):
        font = pygame.font.Font(None, font_size)
        return font.render(text, 1, self.font_color)
            
    def draw(self, screen, mouse):
        if self.visible:
            #if self.response is not None:
            #    if self.response.ready:
            #        self.processresponse()
            #        self.response = None
            self.obj = pygame.draw.rect(screen, self.default_color, (self.x, self.y, self.width, self.height))
            self.joinbutton.draw(screen, mouse, (self.x+30, self.y+225, 100, self.fontsize), (self.x+65, self.y+225+4))
            self.cancelbutton.draw(screen, mouse, (self.x+self.width-130, self.y+225, 100, self.fontsize), (self.x+self.width-130+25, self.y+225+4))
            self.refreshbutton.draw(screen, mouse, ((self.x+(self.width-100)/2), self.y+225, 100, self.fontsize), ((self.x+(self.width-100)/2)+25, self.y+225+4))
            
            screen.blit(self.label("Game Name", self.fontsize), (self.x+34, self.y+4))
            screen.blit(self.label("Player Name", self.fontsize), (self.x+184, self.y+4))
            screen.blit(self.label("Player Side", self.fontsize), (self.x+313, self.y+4))
            screen.blit(self.label("Scenario", self.fontsize), (self.x+408, self.y+4))
            
            pygame.draw.line(screen, self.font_color, (self.x+150, self.y+4), (self.x+150, self.y+220))
            pygame.draw.line(screen, self.font_color, (self.x+300, self.y+4), (self.x+300, self.y+220))
            pygame.draw.line(screen, self.font_color, (self.x+400, self.y+4), (self.x+400, self.y+220))
            pygame.draw.line(screen, self.font_color, (self.x+4, self.y+self.fontsize), (self.x+467, self.y+self.fontsize))
            pygame.draw.line(screen, self.font_color, (self.x+4, self.y+220), (self.x+467, self.y+220))
            
            if self.selectedindex is not None:
                pygame.draw.rect(screen, self.hover_color, (self.x+4, self.y+(self.fontsize*(self.selectedindex+1)), 467, self.fontsize))
            
            for name in self.namelist:
                screen.blit(name[0], name[1])
            for player in self.playerlist:
                screen.blit(player[0], player[1])
            for scenario in self.scenariolist:    
                screen.blit(scenario[0], scenario[1])
            for side in self.sidelist:    
                screen.blit(side[0], side[1])
            
    def drawloading(self, screen):
        screen.blit(self.loadingtext, (self.x+100, self.y+100))
    
    def checkclick(self, mouse):
        if mouse[0] > self.x and mouse[0] < self.x+self.width:
            self.selectedindex = int((mouse[1]-self.y-self.fontsize)/self.fontsize)
            self.selectedgame = self.gamelist[self.selectedindex]
            if self.selectedgame["scenario"] == "egrix":
                self.scenarioflag = False
            else:
                self.scenarioflag = True
            #if self.selectedgame["allegiance"] == "rebel":
            #    self.sideflag = True
    
    def setgamelist(self, gamedict):
        print "Stuff"
        self.gamelist = []
        self.namelist = []
        self.playerlist = []
        self.scenariolist = []
        self.sidelist = []
        for index, game in enumerate(gamedict['response']['games']):
            if index < 10:
                self.gamelist.append(game)
                self.namelist.append((self.label(game["id"], self.fontsize), (self.x+4, self.y+4+((index+1)*self.fontsize))))
                self.playerlist.append((self.label(game["player1"], self.fontsize), (self.x+154, self.y+4+((index+1)*self.fontsize))))
                self.scenariolist.append((self.label(game["scenario"], self.fontsize), (self.x+404, self.y+4+((index+1)*self.fontsize))))
                #self.sidelist.append((self.label(game["allegiance"], self.fontsize), (self.x+304, self.y+4+((index+1)*self.fontsize)))
        self.gamebox = pygame.Rect(self.x, self.y+self.fontsize, self.width, self.fontsize*len(self.namelist))