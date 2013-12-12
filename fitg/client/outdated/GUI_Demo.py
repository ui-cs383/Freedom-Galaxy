#@PydevCodeAnalysisIgnore
import os
import sys
import pygame
import environs
import buttons

pygame.init()

#Global notification log stack
LogStack = []

def main():
    clock = pygame.time.Clock()

    screensize = (1024, 800)
    screen = pygame.display.set_mode(screensize)
    starbg = pygame.image.load("stars.jpg")
    starbg = pygame.transform.scale(starbg, (screensize))
    pygame.mouse.set_visible(0)

    screen.blit(starbg, (0, 0))
    mouseptr = MouseCursor('pointer2.png')
    mousesel = MouseCursor('selected2.png')
    controls = pygame.sprite.RenderUpdates((mouseptr))
    controls.draw(screen)
    pygame.display.flip()

    #===========================================================================
    # Game Control Handling:
    #===========================================================================
    selection = pygame.sprite.LayeredUpdates(())
    unitstack = Stack()
    animate = True
    mouse_update = False
    prev_pos = None
    prev_loc = None

    #===========================================================================
    # Object Initialization:
    #===========================================================================
    purple = Planet('purple', 'purple_planet.png', 'left')
    earth = Planet('earth', 'earth_planet.png', 'center')
    blue = Planet('blue', 'blue_planet.png', 'right')
    cis = Ship('cis', 'rebel_cis.jpg', (100, 200))
    megathron = Ship('megathron', 'rebel_megathron.jpg', (100, 250))
    vagabond1 = Ship('vagabond', 'imperial_vagabond.jpg', (100, 500))
    vagabond2 = Ship('vagabond', 'imperial_vagabond.jpg', (250, 600))
    viper = Ship('viper', 'imperial_viper.jpg', (400, 500))
    #imperialships = pygame.sprite.LayeredUpdates((vagabond1, vagabond2))
    rebelships = pygame.sprite.LayeredUpdates((cis, megathron, viper, vagabond1, vagabond2))
    planets = pygame.sprite.LayeredUpdates((earth, purple, blue))
    starsystem = System('star system', planets, starbg, animate)

    #Menu buttons
    LogButton = buttons.Button()
    CloseLogButton = buttons.Button()
    DetailsButton = buttons.Button()
    CloseDetailsButton = buttons.Button()
    MissionButton = buttons.Button()
    CloseMissionButton = buttons.Button()
    HelpButton = buttons.Button()
    CloseHelpButton = buttons.Button()
    #Mission buttons
    MissionCoup = buttons.Button()
    MissionGI = buttons.Button()
    MissionDip = buttons.Button()
    MissionAssas = buttons.Button()
    MissionSubvert = buttons.Button()
    MissionScavenge = buttons.Button()
    MissionCamp = buttons.Button()
    MissionRebelion = buttons.Button()
    #Initialize the hidden buttons
    CloseLogButton.create_button(screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
    CloseDetailsButton.create_button(screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
    CloseMissionButton.create_button(screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
    CloseHelpButton.create_button(screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
    MissionCoup.create_button(screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
    MissionGI.create_button(screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
    MissionDip.create_button(screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
    MissionAssas.create_button(screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
    MissionSubvert.create_button(screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
    MissionScavenge.create_button(screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
    MissionCamp.create_button(screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))
    MissionRebelion.create_button(screen, (255, 0, 0), 0,  0,    0,    0,   0,    "X", (0, 0, 0))

    while 1:
        clock.tick(60)

        #=======================================================================
        # Event Handling:
        #=======================================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if not mouseptr.down:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    print 'PRINTING UNIT STACK:'  # Testing
                    for sprite_group in unitstack.list:
                        print sprite_group
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouseptr.pressed = mousesel.pressed = True
                        mouseptr.released = mousesel.released = False
                        #=======================================================
                        # Joe's button flags
                        #=======================================================
                        print LogButton.flag
                        buttons.update_buttons(mouseptr.rect, LogStack, LogButton, CloseLogButton, DetailsButton, CloseDetailsButton, HelpButton, CloseHelpButton, MissionButton, CloseMissionButton, 
                                      MissionCoup, MissionGI, MissionDip, MissionAssas, MissionSubvert, MissionScavenge, MissionCamp, MissionRebelion)

                        # check to see if anything has been selected
                        mouse_update, prev_pos, prev_loc = select_check(rebelships, planets, mouseptr, selection, unitstack)
                        # while the mouse button is down, change its cursor
                        controls.remove(mouseptr)
                        controls.add(mousesel)
                    elif event.button == 3:
                        key_mod = pygame.key.get_mods()
                        if key_mod == 4097 or key_mod == 1:
                            left_select_check(rebelships, mouseptr, selection, unitstack, True)
                        else:
                            left_select_check(rebelships, mouseptr, selection, unitstack, False)

            if event.type == pygame.MOUSEBUTTONUP:
                mouseptr.released = mousesel.released = True
                # check to see if something was selected
                if mouse_update and prev_pos is None:  # planet was selected
                    starsystem.planet_move(selection)
                elif mouse_update:  # a unit was selected
                    unit_unselect_check(rebelships, planets, mousesel, prev_pos, prev_loc, selection, unitstack)
                mouse_update = False
                # while the mouse button is up, change its cursor
                controls.remove(mousesel)
                controls.add(mouseptr)

        # Update where the ships are in relation to planets; update controls and selection movement
        planets.update()
        rebelships.update(planets) # bullshit
        controls.update()
        selection.update(mouse_update, animate)

        # Refresh the screen
        screen.blit(starbg, (0, 0))
        planets.draw(screen)
        
        #=======================================================================
        # This needs work
        #=======================================================================
        for planet in planets.sprites():
            #if planet.orient == 'center':
            planet.environment.update()
            planet.environment.draw(screen)
        #=======================================================================
        # This needs work
        #=======================================================================
        
        rebelships.draw(screen)
        for stack in unitstack.list:
            stack.draw(screen)
        #unitstack.draw(screen) # Not working as intended
        selection.draw(screen)

        #=======================================================================
        # Joe's draw buttons
        #=======================================================================
        buttons.draw_buttons(screen, selection,
                            LogStack, LogButton, CloseLogButton,
                            DetailsButton, CloseDetailsButton,
                            HelpButton, CloseHelpButton,
                            MissionButton, CloseMissionButton, MissionCoup, MissionGI, MissionDip,
                            MissionAssas, MissionSubvert, MissionScavenge, MissionCamp, MissionRebelion)

        controls.draw(screen)
        pygame.display.flip()


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


class System():
    def __init__(self, name, planetlist, background, animate=None):
        self.name = name
        self.screen = pygame.display.get_surface()
        self.background = background
        self.planets = planetlist
        self.movedir = None
        self.animate = animate

    def planet_move(self, selectionlist):
        print 'SYSTEM - SELECTION:', selectionlist
        self.movedir = None
        for selectedplanet in selectionlist:
            # Move planets to the right
            if selectedplanet.orient is 'left':
                self.movedir = 'right'
                selectedplanet.update(self.movedir, self.animate)
                for planet in self.planets:
                    planet.update(self.movedir, self.animate)
            # Move planets to the left
            elif selectedplanet.orient is 'right':
                self.movedir = 'left'
                selectedplanet.update(self.movedir, self.animate)
                for planet in self.planets:
                    planet.update(self.movedir, self.animate)
            self.planets.add(selectedplanet)
            selectionlist.empty()
        if self.movedir and self.animate:
            self._planet_animate()

    def _planet_animate(self):
        # These need to be set in the singleton screen class
        curframe = 0    # <--
        frames = 64     # <--
        width = 512     # <--

        # Can this be cleaned up? Yes and it will
        offset = -1     # <--
        offsetadj = -1  # <--
        fill = -1       # <--
        filladj = -1    # <--

        # Move right - wrap around effect
        if self.movedir is 'right':
            while curframe < frames:
                for planet in self.planets:
                    if planet.porient is 'left':
                        planet.rect.move_ip(8, 0)
                    elif planet.porient is 'center':
                        planet.rect.move_ip(8, 0)
                    elif planet.porient is 'right':
                        planet.rect.move_ip(-16, 0)
                self.screen.blit(self.background, (0, 0))
                self.planets.draw(self.screen)
                pygame.display.flip()
                curframe += 1

        # Move left - slide from off screen effect
        elif self.movedir is 'left':
            while curframe < frames:
                for planet in self.planets:
                    if planet.porient is 'left':
                        offset = planet.rect.midright[0] - planet.rect.center[0]
                        fill = width - 2 * offset
                        if planet.rect.midright[0] >= 0 and planet.rect.midleft[0] < width:
                            planet.rect.move_ip(-8, 0)
                            filladj = fill
                        elif filladj >= 0:
                            filladj -= 8
                            planet.rect.midleft = self.screen.get_rect().midright
                            offsetadj = offset
                        elif offsetadj >= 0:
                            offsetadj -= 8
                            planet.rect.move_ip(-8, 0)
                    elif planet.porient is 'center':
                        planet.rect.move_ip(-8, 0)
                    elif planet.porient is 'right':
                        planet.rect.move_ip(-8, 0)
                self.screen.blit(self.background, (0, 0))
                self.planets.draw(self.screen)
                pygame.display.flip()
                curframe += 1
        self.planets.update()


class Planet(pygame.sprite.Sprite):
    def __init__(self, name, image, orientation):
        self.name = name
        self.orient = orientation  # Where the planet is in relation to the screen
        self.poreint = orientation  # Previous orientation
        self.screen = pygame.display.get_surface()
        if self.orient is 'left':
            self.pos = self.screen.get_rect().midleft
        elif self.orient is 'center':
            self.pos = self.screen.get_rect().center
        elif self.orient is 'right':
            self.pos = self.screen.get_rect().midright
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image, -1)
        self.rect.center = self.pos
        self.colliderect = self.rect.inflate(-50, -50)
        self.colliderect.normalize()
        #=======================================================================
        # The environs will be populated by the backend - we'll need to expand
        # the planet class to take more variables.
        #=======================================================================
        self.environment = environs.EnvironBox(self.rect)
        self.environment.addEnviron(1, 'W', 4, "Humans", 4, "Animals", 'C' )
        self.environment.addEnviron(2, 'U', 4, "Humans", 4, "Animals", 'C' )
        self.environment.addEnviron(3, 'F', 3, "H", 2, "A", 'A')

    def update(self, movedir=None, animate=None):  # Update planet orientation
        self.porient = self.orient
        if movedir is 'right':
            if self.orient is 'left':
                self.pos = self.screen.get_rect().center
                self.orient = 'center'
            elif self.orient is 'center':
                self.pos = self.screen.get_rect().midright
                self.orient = 'right'
            elif self.orient is 'right':
                self.pos = self.screen.get_rect().midleft
                self.orient = 'left'
            if not animate:
                self.rect.center = self.pos
                self.colliderect.center = self.pos
        elif movedir is 'left':
            if self.orient is 'left':
                self.pos = self.screen.get_rect().midright
                self.orient = 'right'
            elif self.orient is 'center':
                self.pos = self.screen.get_rect().midleft
                self.orient = 'left'
            elif self.orient is 'right':
                self.pos = self.screen.get_rect().center
                self.orient = 'center'
            if not animate:
                self.rect.center = self.pos
                self.colliderect.center = self.pos
        else:
            self.rect.center = self.pos
            self.colliderect.center = self.pos
            #self.environment.update()


class Ship(pygame.sprite.Sprite):
    def __init__(self, name, image, position):
        self.name = name
        self.pos = position
        self.loc = None
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image, -1)
        self.rect.center = self.pos

    def update(self, bullshit, selected=None, animate=None):  # ship animation will be added later
        if selected:
            self.pos = pygame.mouse.get_pos()
            self.rect.center = self.pos
        else:
            try:
                if self.pos[0] is 'x':
                    #print 'HELLO'
                    # get the information for the specified environ, then set the pos[0] and pos[1] according to the list of collidepopints
                    move = bullshitfunction(bullshit, self.loc, self.pos)
                    self.rect.center = move
                else:
                    self.rect.clamp_ip(self.loc)
            except:
                #print 'WARNING:', self.name, 'is drifting - put it on a planet'
                return


class Stack():
    def __init__(self):
        self.list = []
        self.refresh = False

    def make(self, unit):
        print 'MAKING NEW STACK'  # Testing
        sprite_group = pygame.sprite.LayeredUpdates((unit))
        self.list.append(sprite_group)
        return sprite_group

    def add(self, unit, unitstack):
        for stack in self.list:
            if stack.has(unitstack):
                stack.add(unit)

    def remove(self, unit):
        for stack in self.list:
            if stack.has(unit):
                print 'REMOVING'  # Testing
                sprite = stack.get_top_sprite()
                sprite.rect.move_ip(0, -50)
                stack.remove(sprite)
                if len(stack) == 1:
                    self.list.remove(stack)

    def has(self, unit):
        for stack in self.list:
            if stack.has(unit):
                return True

    def cycle(self, unit):
        for stack in self.list:
            if stack.has(unit):
                sprite = stack.get_top_sprite()
                stack.move_to_back(sprite)
                self.refresh = True
                return

    def sprites(self, unit):
        for stack in self.list:
            if stack.has(unit):
                return stack.sprites()

    def update(self, unit, location):
        for stack in self.list:
            if stack.has(unit):
                self.refresh = True
                for sprite in stack:
                    sprite.pos = unit.pos # I call bullshit
                    sprite.loc = location
                    sprite.rect.clamp_ip(location)

    def draw(self, screen):
        if self.refresh:
            print 'REDRAWING'  # Testing
            for stack in self.list:
                print stack
                stack.draw(screen)
            self.refresh = False

    def highlight(self, mouse):
        for stack in self.list:
            for collision in pygame.sprite.spritecollide(mouse, stack, False):
                print collision.name


def bullshitfunction(planetlist, planet_rect, location_list):
    #print 'KNEE DEEP IN SHIT'
    for planet in planetlist:
        if planet.rect.center == planet_rect.center:
            for environment in planet.environment.environlist:
                if environment.number == location_list[1]:
                    return environment.collidepoints[location_list[2]]


# Will be added to the mouse class
def select_check(unitlist, planetlist, mouse, selectionlist, unitstack):
    for unit in unitlist:
        if unit.rect.collidepoint(mouse.pos):
            if unitstack.has(unit):
                selectionlist.add(unitstack.sprites(unit))
                print 'SELECTED STACK: ', selectionlist, mouse.pos  # Testing
                LogStack.insert(0,"Unit: "+str(selectionlist)+" selected")
                return True, unit.rect.center, unit.loc
            else:
                selectionlist.add(unit)
                print 'SELECTED: ', selectionlist, mouse.pos  # Testing
                unitlist.remove(unit)
                LogStack.insert(0,"Unit: "+str(selectionlist)+" selected")
                return True, unit.rect.center, unit.loc
    for planet in planetlist:
        if planet.rect.collidepoint(mouse.pos):
            print 'SELECTED: ', planet.name  # Testing
            selectionlist.add(planet)
            planetlist.remove(planet)
            LogStack.insert(0,"Planet: "+planet.name+" selected")
            return True, None, None
    return False, None, None


# Will be added to the mouse class
def left_select_check(unitlist, mouse, selectionlist, unitstack, breakstack):
    if breakstack:
        for unit in unitlist:
            if unit.rect.collidepoint(mouse.pos):
                if unitstack.has(unit):
                    unitstack.remove(unit)
                    return True
    else:
        for unit in unitlist:
            if unit.rect.collidepoint(mouse.pos):
                unitstack.cycle(unit)
                return True


# Will be added to the mouse class
def unit_unselect_check(unitlist, planetlist, mouse, prev_pos, prev_loc, selectionlist, unitstack):
    for unit in selectionlist:
        if unitstack.has(unit):
            print 'UNSELECTING STACK'  # Testing
            for planet in planetlist:
                #===============================================================
                # This needs work
                #===============================================================
                if planet.environment.addunits(selectionlist):
                    'STACK LANDING ON ENVIRON:'
                    unitstack.update(unit, planet.colliderect)
                    selectionlist.empty()
                    return True
                if planet.rect.collidepoint(mouse.pos):
                    print 'STACK LANDING ON:', planet.name  # Testing
                    unitstack.update(unit, planet.colliderect)
                    selectionlist.empty()
                    return True
            unit.pos = prev_pos
            unit.rect.center = unit.pos
            unit.loc = prev_loc
            selectionlist.empty()
        else:
            print 'UNSELECTING SINGLE'  # Testing
            if _unit_stack_check(unitlist, unit, selectionlist, unitstack):
                    return True
            for planet in planetlist:
                #===============================================================
                # This needs work
                #===============================================================
                if planet.environment.addunits(selectionlist):
                    'SINGLE LANDING ON ENVIRON:'
                    unitlist.add(unit)
                    selectionlist.empty()
                    return True
                if planet.rect.collidepoint(mouse.pos):
                    print 'SINGLE LANDING ON:', planet.name  # Testing
                    unit.loc = planet.colliderect  # set the location of the ship to the planet !!
                    unit.rect.clamp_ip(planet.colliderect)
                    unitlist.add(unit)
                    selectionlist.empty()
                    return True
            unit.pos = prev_pos
            unit.rect.center = unit.pos
            unit.loc = unit.loc
            unitlist.add(unit)
            selectionlist.empty()
            return False


# Will be added to the mouse class
def _unit_stack_check(unitlist, selunit, selectionlist, unitstack):
    # if there are stacks present on the stack list, is the unit joining one of these existing stacks?
    for stack in unitstack.list:
        for collision in pygame.sprite.spritecollide(selunit, stack, False):
            selunit.pos = collision.pos
            selunit.loc = collision.loc
            selunit.rect.clamp_ip(collision.rect)
            unitstack.add(selunit, stack)
            unitlist.add(selunit)
            selectionlist.empty()
            unitstack.cycle(selunit)
            return True
    # if the unit is not joining an existing stack, create a new stack and append the stack onto the stack list.
    for unit in unitlist:
        if selunit.rect.colliderect(unit.rect):
            selunit.pos = unit.rect.center
            selunit.loc = unit.loc
            selunit.rect.clamp_ip(unit.rect)
            unitstack.add(unit, unitstack.make(selunit))
            unitlist.add(selunit)
            selectionlist.empty()
            unitstack.cycle(selunit)
            return True
    return False


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
        image.set_colorkey(colorkey)  # pygame.RLEACCEL can improve performance
    return image, image.get_rect()

if __name__ == '__main__':
    main()
