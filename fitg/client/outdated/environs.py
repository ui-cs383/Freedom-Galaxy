import os
import sys
import pygame
from math import pi, cos, sin

ETcolors = { 'U' : (150,150,150), 'F' : (200, 0, 0), 'W' : (50, 150, 50)}
STARTANGLE = pi / 2
UNITANGLE = pi / 8
LINECOLOR = (0,200,0)


class Environ():
    def __init__(self, center, iradius, oradius, number, type, size, race, resources, creature, politics):
        self.box = pygame.Rect(center[0] - oradius, center[1] - oradius, oradius * 2, oradius * 2)
        self.number = number
        self.type = type
        self.size = size
        self.race = race
        self.resources = resources
        self.creature = creature
        self.politics = politics
        self.startangle = STARTANGLE + (self.number * UNITANGLE)
        self.endangle = self.startangle + UNITANGLE
        self.iradius = iradius
        self.oradius = oradius
        self.averadius = (iradius + oradius) / 2
        self.center = center
        #print center
        #self.colliderect = pygame.Rect(,,,)
        self.getcolor(type)
        self.collidepoints = []
        self.updatepoints()

    def __str__(self):
        return str(self.number)

    def getcolor(self, type):
        self.fillcolor = ETcolors[type]

    def shiftdown1(self):
        self.endangle = self.endangle + UNITANGLE
        self.startangle = self.startangle + UNITANGLE
        self.updatepoints()

    def shiftup1(self):
        self.endangle = self.endangle - UNITANGLE
        self.startangle = self.startangle - UNITANGLE
        self.updatepoints()

    def expand1(self):
        self.endangle = self.endangle + UNITANGLE
        self.updatepoints()
        print 'Expanding'
        print self.collidepoints[-2]
        return pygame.Rect(self.collidepoints[-2], (1, 1))

    def contract1(self):
        self.endangle = self.endangle - UNITANGLE
        #self.updatepoints()

    def updatepoints(self):
        self.collidepoints = []
        angle = self.startangle
        while angle < self.endangle:
            angle = angle + UNITANGLE / 2
            self.collidepoints.append((int(self.center[0] + (cos(angle) * self. averadius)), int(self.center[1] - (sin(angle) * self. averadius))))
            angle = angle + UNITANGLE / 2
        self.stacks = len(self.collidepoints)

    def update(self, stacklist):
        self.total = self.stacks
        for stack in stacklist:
            for point in self.collidepoints:
                for sprite in stack.sprites():
                    if sprite.rect.collidepoint(point):
                        self.total = self.total + 1
                    else:
                        self.total = self.total - 1
                        #stacklist.remove(stack)
        for i in range(self.stacks - self.total):
            if i > 0:
                self.contract1();
        #print 'total: '+str(self.total)
        #print 'stacks: '+str(self.stacks)
        self.updatepoints()
        #for stack in stacklist:
        #    for point in self.collidepoints:
        #        if stack.rect.collidepoint(point):
        #            stack.pos = point
        #            stack.update()
        return self.stacks - self.total  #amount of growth/shrinkage

    def draw(self, surface):
        pygame.draw.line(surface, self.fillcolor, (self.center[0]+self.oradius*(cos(self.startangle)), self.center[1]-self.oradius*(sin(self.startangle))), (self.center[0]+self.iradius*(cos(self.startangle)), self.center[1]-self.iradius*(sin(self.startangle))), 2)
        pygame.draw.line(surface, self.fillcolor, (self.center[0]+self.oradius*(cos(self.endangle)), self.center[1]-self.oradius*(sin(self.endangle))), (self.center[0]+self.iradius*(cos(self.endangle)), self.center[1]-self.iradius*(sin(self.endangle))), 4)
        pygame.draw.arc(surface, self.fillcolor, pygame.Rect(self.box.topleft, (2*self.oradius, 2*self.oradius)), self.startangle, self.endangle+pi/72, 3)
        pygame.draw.arc(surface, self.fillcolor, pygame.Rect(self.box.topleft[0]+(self.oradius-self.iradius), self.box.topleft[1]+(self.oradius-self.iradius), 2*self.iradius, 2*self.iradius), self.startangle, self.endangle + pi/72, 3)
        for point in self.collidepoints:
            #print 'point: '
            #print point[0]
            #print point[1]
            pygame.draw.circle(surface, LINECOLOR, point, 5)
        #pygame.draw.rect (surface, LINECOLOR, self.box, 1)


class EnvironBox():
    def __init__(self, planetrect):
        #self.name = name
        self.planet = planetrect
        self.environlist = []
        self.envarc = pygame.Rect(planetrect.topleft[0] - 75, planetrect.topleft[1] - 75, planetrect.width + 150, planetrect.height + 150)
        self.stacklist = []
#        self.firstangle = 2*pi/3
#        self.lastangle = 2*pi/3

    def addEnviron(self, number, type, size, race, resources, creature, politics):
        self.environlist.append(Environ(self.planet.center, self.planet.width / 2 + 50, self.planet.width / 2 + 150, number, type, size, race, resources, creature, politics))

    def addunits(self, unitlist):
        #=======================================================================
        # Sean's addition
        #=======================================================================
        for unit in unitlist:
            for environ in self.environlist:
                print 'Checking Environ: ' + str(environ)
                for point in environ.collidepoints:  # collidepoints - a list of points within an environment
                    print 'Checking Collidepoint: ' + str(point)

                    #if (stack.has(unit)):
                    #    if (stack.list[0].get_top_sprite().rect.collidepoint(j)):
                    #        for spritegroup in stack.list:
                    #            self.stacklist.append(spritegroup)
                    #        stack.update( unit, i.expand1())
                    #        for k in self.environlist[i.number:]:
                    #            k.shiftdown1()
                    #        return i.number
                    #else:

                    if (unit.rect.collidepoint(point)):
                        for list_position, environ_collidepoint in enumerate(environ.collidepoints):
                            if environ_collidepoint[0] == point[0] and environ_collidepoint[1] == point[1]:
                                print list_position, environ.number # Testing
                                #===============================================
                                # This should not be happening here....
                                #===============================================
                                location = ('x', environ.number, list_position)
                                unit.loc = self.planet
                                unit.pos = location
                                ################################################
                        environ.expand1()
                        for k in self.environlist[environ.number:]:
                            k.shiftdown1()
                        return True
        return False
        # self.lastangle = self.lastangle + UNITANGLE

    def update(self):
        #self.envarc.collidelist(stacklist)
        for i in self.environlist:
            i.center = self.planet.center
            i.box.center = i.center
            ret = i.update(self.stacklist)

            #print 'return: '+str(ret)
            if (ret != 0):
                for j in range(0, ret):
                    for k in self.environlist[i.number:]:
                        if (j > 0):
                            k.shiftup1()
                        if (j < 0):
                            k.shiftdown1()
            #self.outsideArc = [self.rect, ARCCOLOR, self.rect, self.firstangle, self.lastangle]
            #self.insideArc = [self.rect, ARCCOLOR, self.rect, self.firstangle, self.lastangle]

    def draw(self, surface):
        for i in self.environlist:
            i.draw(surface)
        #pygame.draw.arc(self.outsideArc)
        #pygame.draw.arc(self.insideArc)