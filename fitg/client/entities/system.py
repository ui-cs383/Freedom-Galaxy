import pygame
from math import log10
from unit import Unit
from planet import Planet

class System():
    def __init__(self, screen, background, animate=None, characterlist=None, planetlist=None, environlist=None, militarylist=None, stacklist=None):
        self.screen = screen
        self.background = background
        self.id = 22
        self.animate = animate
        self.move_dir = None
        #=======================================================================
        # Planet Population
        #=======================================================================
        purple = Planet(self, planetlist[0], environlist, "left", "purple_planet.png")
        earth = Planet(self, planetlist[1], environlist, "center", "earth_planet.png")
        blue = Planet(self, planetlist[2], environlist, "right", "blue_planet.png")
        self.planet_list = pygame.sprite.LayeredUpdates((purple, earth, blue))
        #planet_locs = dict(planetlist[0]["id"]: planetlist[0]["location"], planetlist[1]["id"]: planetlist[1]["location"], planetlist[2]["id"]: planetlist[2]["location"])
        #print planetlist
        self.planet_locs = dict()
        self.environ_locs = dict()
        for planet in planetlist:
            self.planet_locs[str(planet["id"])] = int(planet["location"])*10
        #print self.planet_locs
        for environ in environlist:
            #print environ["planet_id"]
            self.environ_locs[environ["id"]] = self.planet_locs[str(environ["planet_id"])]+environ["location"]
        #print self.environ_locs
            
        #=======================================================================
        # Unit Population
        #=======================================================================
        
        self.unit_list = pygame.sprite.LayeredDirty()
        print "Starting length: " + str(len(self.unit_list.sprites()))
        for character in characterlist:
            #print character
            self.addunit(True, character)
            
        for milunit in militarylist:
            #print milunit
            self.addunit(False, milunit)
        
        for stack in stacklist:
            for unit in self.unit_list:
                if unit.stack_id == stack["id"]:
                    unit.set_loc_id(self.environ_locs[stack["environ_id"]])


    def addunit (self, charflag, unitdict):
        newunit = Unit(charflag, unitdict)
        createnewstack = True
        #self.unit_list.add(newunit)
        #print "Length: " + str(len(self.unit_list.sprites()) )
        if len(self.unit_list.sprites()) == 0:
            print "First unit"
            self.unit_list.add(newunit)
        else:
            for unit in self.unit_list:
                print "unit's stack id: " + str(unit.stack_id)
                print "new unit's stack id: " + str(newunit.stack_id)
                if newunit.stack_id == unit.stack_id:
                    print "Adding unit "+ str(newunit.id) + " to stack " + str(unit.stack_id) + "char?: " + str(charflag)
                    print "---"
                    unit.add_unit(newunit)
                    createnewstack = False
                    break
            if createnewstack:
                print "New stack for "+ str(unit.id) + " for stack " + str(unit.stack_id) + "char?: " + str(charflag)
                print "---"
                self.unit_list.add(newunit)
                    
        
        
    def update(self):
        for planet in self.planet_list:
            planet.update()
            planet.environment.update()
        self._update_unit_location()
        for unit in self.unit_list:
            unit.update()

    def draw(self):
        self.planet_list.draw(self.screen)
        for planet in self.planet_list:
            if planet.orient is "center":
                planet.environment.draw(self.screen)
                break
        self.unit_list.draw(self.screen)

    def planets_move(self, planet):
        self.move_dir = None
        # Move planets to the right
        if planet.orient is "left":
            self.move_dir = "right"
            self.planet_list.move_to_front(planet)
            for planet in self.planet_list:
                planet.update(self.move_dir, self.animate)
        # Move planets to the left
        elif planet.orient is "right":
            self.move_dir = "left"
            self.planet_list.move_to_front(planet)
            for planet in self.planet_list:
                planet.update(self.move_dir, self.animate)
        if self.move_dir and self.animate:
            self._planets_animate()

    def _planets_animate(self):
        # These need to be set in the singleton screen class
        cur_frame = 0    # <--
        frames = 64      # <--

        if self.move_dir is "right":
            while cur_frame < frames:
                for planet in self.planet_list:
                    if planet.prev_orient is "left":
                        planet.rect.move_ip(8, 0)
                    elif planet.prev_orient is "center":
                        planet.rect.move_ip(8, 0)
                    elif planet.prev_orient is "right":
                        planet.rect.move_ip(-16, 0)
                self.screen.blit(self.background, (0, 0))
                self.planet_list.draw(self.screen)
                pygame.display.flip()
                cur_frame += 1
        elif self.move_dir is "left":
            while cur_frame < frames:
                for planet in self.planet_list:
                    if planet.prev_orient is "left":
                        planet.rect.move_ip(16, 0)
                    elif planet.prev_orient is "center":
                        planet.rect.move_ip(-8, 0)
                    elif planet.prev_orient is "right":
                        planet.rect.move_ip(-8, 0)
                self.screen.blit(self.background, (0, 0))
                self.planet_list.draw(self.screen)
                pygame.display.flip()
                cur_frame += 1
        self.update()

    def _update_unit_location(self):
        for unit in self.unit_list:
            loc_id = unit.loc_id
            #print "Location of unit: " + str(loc_id)
            unit.visible = 1
            if loc_id:
                digits = len(str(loc_id))
                #print digits
                if digits >= 4:
                    #print "digits >= 4"
                    environ_id = loc_id % 10
                    planet_id = loc_id / 10
                elif digits >= 3:
                    planet_id = loc_id / 10
                elif digits >= 2:
                    self.system_id = loc_id % 10
                #loc_id /= 10
            #print "Resolved loc_id: " + str(loc_id)
            for planet in self.planet_list:
                if planet.location == planet_id:
                    if environ_id == 0:
                        unit.pos = None
                        unit.loc = planet.collide_rect
                    else:
                        if planet.orient is "center":
                            for point in planet.environment.environ_list[environ_id - 1].collision_points:
                                if unit.rect.colliderect(pygame.Rect((point), (2, 2))):
                                    unit.pos = point
                                    unit.loc = None
                                    unit.update()
                                    break
                                else:
                                    if len(self.unit_list.get_sprites_at(point)) == 0:
                                        unit.pos = point
                                        unit.loc = None
                                        unit.update()
                                        break
                        else:
                            unit.visible = 0
                            break
