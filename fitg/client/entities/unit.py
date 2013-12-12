import pygame
from support.loadimage import load_image


class Unit(pygame.sprite.DirtySprite):
    __slots__ = ['id', 'stack_id', 'side', 'endurance', 'charflag',
                 'name', 'mobile', 'environ_combat', 'space_combat',
                 'image', 'rect', 'detected', 'wounds', 'active',
                 'bonuses', 'title', 'race', 'combat', 'intelligence',
                 'leadership', 'diplomacy', 'navigation', 'homeworld',
                 'detected', 'captive' 'loc_id', 'pos', 'loc', 'stack_id',
                 'prev_image', 'dirty', 'stack_list', 'environ_id']
    def __init__(self, charflag, unitdict):
        pygame.sprite.DirtySprite.__init__(self)
        for prop in ['id', 'stack_id', 'side']:#, 'environ_id']:
            setattr(self, prop, unitdict[prop])
        
        if charflag is False:
            self.charflag = charflag
            self.name = unitdict["type"]
            for prop in ['mobile', 'environ_combat', 'space_combat', 'stack_id']:
                setattr(self, prop, unitdict[prop])
            self.image, self.rect = load_image("DrJ.png")
            
        if charflag is True:
            properties = ('name', 'detected', 'wounds', 'active', 'stack_id',
                          'bonuses', 'title', 'race', 'combat', 'intelligence',
                          'leadership', 'diplomacy', 'navigation', 'homeworld',
                          'detected', 'captive')
            for prop in properties:
                setattr(self, prop, unitdict[prop])
            self.image, self.rect = load_image(unitdict["img"]) 
        self.loc_id = 2210
        self.pos = None
        self.loc = None
        self.prev_image = self.image
        self.dirty = 2
        self.stack_list = list()
        self.stack_list.append(self)

    def set_stack_id (self, new_stack_id):
        for unit in self.stack_list:
            unit.stack_id = new_stack_id
            
    def set_loc_id (self, new_loc_id):
        for unit in self.stack_list:
            unit.loc_id = new_loc_id
            
    def set_environ_id (self, new_environ_id):
        for unit in self.stack_list:
            unit.environ_id = new_environ_id
    
    def cycle_unit(self):
        if len(self.stack_list) > 1:
            sprite = self.stack_list.pop()
            self.stack_list.insert(0, sprite)
            if sprite == self:
                self.image = self.prev_image
            else:
                self.image = sprite.image

    def add_unit(self, sprite):
        #sprite.visible = 0
        #sprite.loc_id = self.loc_id
        #sprite.pos = self.pos
        #sprite.loc = self.loc
        sprite.set_stack_id(self.stack_id)
        self.stack_list.extend(sprite.stack_list)
        sprite.stack_list = list()
        for sprite in self.stack_list:
            sprite.image = sprite.prev_image

    def remove_unit(self):
        if len(self.stack_list) > 1:
            sprite = self.stack_list.pop()
            if sprite == self:
                self.stack_list.insert(0, self)
                sprite = self.stack_list.pop()
            if len(self.stack_list) == 1:
                self.image = self.prev_image
            sprite.visible = 1
            sprite.loc_id = self.loc_id
            sprite.pos = self.pos
            sprite.loc = self.loc
            sprite.stack_list.append(sprite)
            return sprite
        else:
            return None

    def update(self, selected=None, animate=None):
        if selected:
            self.pos = pygame.mouse.get_pos()
            self.rect.center = self.pos
        else:
            try:
                if self.loc:
                    self.rect.clamp_ip(self.loc)
                else:
                    self.rect.center = self.pos
            except:
                #print "ERROR:", self.name, "is drifting"
                return
