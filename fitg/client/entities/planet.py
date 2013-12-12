import pygame
import environments
from support.loadimage import load_image


class Planet(pygame.sprite.Sprite):
    def __init__(self, parent_system, planetdict, environlist, planet_orientation, image):
        #print planetdict
        self.parent = parent_system
        #self.
        self.location = planetdict["location"]
        self.planet_id = planetdict["id"]
        self.name = planetdict["name"]
        self.pdb_state = planetdict["pdb_state"]
        self.loyalty = planetdict["loyalty"]
        self.pdb_level = planetdict["pdb_level"]
        self.environ_count = planetdict["environ_count"]
        self.orient = planet_orientation
        self.prev_orient = None
        if self.orient is "left":
            self.pos = self.parent.screen.get_rect().midleft
        elif self.orient is "center":
            self.pos = self.parent.screen.get_rect().center
        elif self.orient is "right":
            self.pos = self.parent.screen.get_rect().midright
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image, -1)
        self.collide_rect = self.rect.inflate(-50, -50)
        #=======================================================================
        # Environment Population
        #=======================================================================
        self.environment = environments.EnvironBox(self, self.rect)
        for environ in environlist:
            #print environ
            if environ["planet_id"] == self.planet_id:
                self.environment.addEnviron(environ)
        #self.environment.addEnviron(1, 'W', 2, "Humans", "Animals", 'C')
        #self.environment.addEnviron(2, 'U', 1, "Bricktons", "Animals", 'C')
        #self.environment.addEnviron(3, 'F', 3, "Corruptons", "Animals", 'A')

    def update(self, move_dir=None, animate=None):
        self.prev_orient = self.orient
        if move_dir is "right":
            if self.orient is "left":
                self.pos = self.parent.screen.get_rect().center
                self.orient = "center"
            elif self.orient is "center":
                self.pos = self.parent.screen.get_rect().midright
                self.orient = "right"
            elif self.orient is "right":
                self.pos = self.parent.screen.get_rect().midleft
                self.orient = "left"
            if not animate:
                self.rect.center = self.pos
                self.collide_rect.center = self.pos
        elif move_dir is "left":
            if self.orient is "left":
                self.pos = self.parent.screen.get_rect().midright
                self.orient = "right"
            elif self.orient is "center":
                self.pos = self.parent.screen.get_rect().midleft
                self.orient = "left"
            elif self.orient is "right":
                self.pos = self.parent.screen.get_rect().center
                self.orient = "center"
            if not animate:
                self.rect.center = self.pos
                self.collide_rect.center = self.pos
        else:
            self.rect.center = self.pos
            self.collide_rect.center = self.pos