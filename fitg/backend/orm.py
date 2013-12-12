#Author: Jeff Crocker
#Purpose: The Object Relational Mapping for the Freedom.db

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
import pyconfig

db = pyconfig.get('database')
path = pyconfig.get('database_path')

engine = create_engine(db + '://' + path)
Base = declarative_base(bind=engine)
Session = scoped_session(sessionmaker(engine))

class Game(Base):
	__tablename__ = 'games'
	id = Column(String, primary_key=True)
	player1 = Column(String)
	player2 = Column(String)
	scenario = Column(String) # this should eventually be tied to a scenario table?
	stacks = relationship("Stack", backref=backref("game", uselist=False))
	planets = relationship("Planet", backref=backref("game", uselist=False))
	phasing_player = Column(String)
	segment = Column(String)

	def __init__(self, id, player1, player2, scenario):
		self.id = id
		self.player1 = player1
		self.player2 = player2
		self.scenario = scenario
		self.phasingplayer = 'Rebel'
		self.segment = 'movement'

	def __repr__(self):
		return "<Game('%s','%s', '%s', '%s')>" % (self.name, self.player1, self.player2, self.scenario)

	def advance_segment(self):
		pass

class Character(Base):
	__tablename__ = 'characters'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String)                       #name of every character
	img = Column(String)                        #Does the DB need this?
	title = Column(String)                      #Long title of character
	race = Column(String)                       #Character's Race
	side = Column(String)                       #Team: 'Rebel' or 'Emperial'
	combat = Column(Integer)                    #Combat strength
	endurance = Column(Integer)                 #Endurance rating
	intelligence = Column(Integer)              #Intelligence rating
	leadership = Column(Integer)                #Leadership rating
	diplomacy = Column(Integer)                 #Diplomacy rating
	navigation = Column(Integer)                #Navigation rating
	homeworld = Column(String)                  #Character's Homeworld
	bonuses = Column(String)                    #Special Bonuses, unclear format
	wounds = Column(Integer)                    #Num of wounds
	detected = Column(Boolean)                  #               
	active = Column(Boolean)
	captive = Column(Boolean)
	stack_id = Column(Integer, ForeignKey('stacks.id'))
	
	def __init__(self, name, img, title, race, side, 
				combat, endurance, intelligence, leadership, diplomacy, 
				navigation, homeworld, bonuses) :
		self.name = name
		self.img = img
		self.title = title
		self.race = race
		self.side = side
		self.combat = combat
		self.endurance = endurance
		self.intelligence = intelligence
		self.leadership = leadership
		self.diplomacy = diplomacy
		self.navigation = navigation
		self.homeworld = homeworld
		self.bonuses = bonuses
		self.wounds = 0
		self.detected = False
		self.possession = False
		self.active = True
		self.captive = False
		
	def __repr__(self):
		return "<Character('%s','%s', '%s')>" % (self.name, self.title, self.side)

				
class Environ(Base):
	__tablename__ = 'environs'
	id = Column(Integer, primary_key=True, autoincrement=True)
	location = Column(Integer) 
	type = Column(String)                   
	size = Column(Integer)                  
	star_faring = Column(Integer)            
	resources = Column(Integer)             
	star_resources = Column(Integer)         
	monster = Column(String)                
	coup = Column(Boolean)                  
	sov = Column(Integer)                   
	planet_id = Column(Integer, ForeignKey('planets.id'))
	race_name = Column(String, ForeignKey('races.name'))
	race = relationship("Race", backref=backref("races", uselist=False))
	stacks = relationship("Stack", backref=backref("environ", uselist=False))

	def __init__(self, location, type, size, race_name, star_faring, resources, 
				star_resources, monster, sov) :
		self.location = location
		self.type = type
		self.size = size
		self.race_name = race_name
		self.star_faring = star_faring
		self.resources = resources
		self.star_resources = star_resources
		self.monster = monster
		self.coup = False
		self.sov = sov
	  
	def __repr__(self):
		return "<Environ('%s','%s', '%s')>" % (self.id, self.type, self.size)

class Unit(Base):
	__tablename__ = 'units'
	id = Column(Integer, primary_key=True, autoincrement=True)
	side = Column(String)     
	type = Column(String)   
	environ_combat = Column(Integer)
	space_combat = Column(Integer)
	mobile = Column(Boolean) 
	stack_id = Column(Integer, ForeignKey('stacks.id'))
	
	def __init__(self, type, side, environ_combat, space_combat, mobile):
		self.type = type
		self.side = side
		self.environ_combat = environ_combat
		self.space_combat = space_combat
		self.mobile = mobile
		
	def __repr__(self):
		return "<Unit('%s','%s', '%s')>" % (self.id, self.type, self.side)

class Mission(Base):
	__tablename__ = 'missions'
	id = Column(Integer, primary_key=True, autoincrement=True)
	side = Column(String)     
	type = Column(String)
	stack_id = Column(Integer, ForeignKey('stacks.id'))
	stack = relationship("Stack", backref=backref('mission', order_by=id))

	def __init__(self, type, stack_id):
		self.type = type
		self.stack_id = stack_id

	def __repr__(self):
		return "<Mission('%s','%s', '%s')>" % (self.id, self.type, self.stack_id)

class Planet(Base):
	__tablename__ = 'planets'
	id = Column(Integer, primary_key=True, autoincrement=True)
	control = Column(String)
	pdb_level = Column(Integer)
	pdb_state = Column(Integer) 
	location = Column(Integer)
	name = Column(String)             
	loyalty = Column(Integer)         
	environ_count = Column(Integer)
	game_id = Column(String, ForeignKey('games.id'))
	environs = relationship("Environ", backref="planet")
	in_rebellion = Column(Boolean)
	was_rebellion = Column(Boolean)    

	def __init__(self, control, pdb_level, pdb_state, location, name, loyalty, environ_count):
		self.pdb_level = pdb_level
		self.pdb_state = pdb_state
		self.control = control
		self.location = location
		self.name = name
		self.loyalty = loyalty
		self.environ_count = environ_count
		self.in_rebellion = False
		self.was_rebellion = False
		
	def __repr__(self):
		return "<Planet('%s','%s', '%s')>" % (self.id, self.name, self.environs)

	def pdb_change(self, val):
		self.pdb_level += val
		if self.pdb_level < 0:
			self.pdb_level = 0
		elif self.pdb_level > 2:
			self.pdb_level = 2:

class Possession(Base):
	__tablename__ = 'possessions'
	id = Column(Integer, primary_key=True, autoincrement=True)
	type = Column(String)                   #Type of possession.
	name = Column(String) #Name of possession.
	img = Column(String)                    #gif related to the possession.
	stat1 = Column(Integer)                  #First stat.
	stat2 = Column(Integer)                  #Second stat.
	stat3 = Column(Integer)                  #Third stat.
	stat4 = Column(Integer)                  #Fourth stat.
	damaged = Column(Boolean)               #Whether the possession is damaged. This really only applies to starships.
	owner_name = Column(String, ForeignKey('characters.name'))
	owner = relationship("Character", backref=backref('possessions', order_by=name))   
	def __init__(self, type, name, img, stat1, stat2, stat3, stat4, owner_name) :
		self.type = type
		self.name = name
		self.img = img
		self.stat1 = stat1
		self.stat2 = stat2
		self.stat3 = stat3
		self.stat4 = stat4
		self.owner_name = owner_name
		self.damaged = False
		
	def __repr__(self):
		return "<Possession('%s','%s', '%s')>" % (self.type, self.name, self.stat1)
				
class Race(Base):
	__tablename__ = 'races'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String, primary_key=True)
	environ = Column(String)               
	combat = Column(Integer)               
	endurance = Column(Integer)            
	firefight = Column(Boolean)            

	def __init__(self, name, environ, combat, endurance, firefight):
		self.name = name
		self.environ = environ
		self.combat = combat
		self.endurance = endurance
		self.firefight = firefight
		
	def __repr__(self):
		return "<Race('%s','%s', '%i')>" % (self.name, self.environ, self.combat)
		
class Stack(Base):
	__tablename__ = 'stacks'

	id = Column(Integer, primary_key=True, autoincrement=True)
	environ_id = Column(Integer, ForeignKey('environs.id'))
	game_id = Column(String, ForeignKey('games.id'))
	characters = relationship('Character', backref='stack')
	units = relationship('Unit', backref='stack')

	def __init__(self):
		pass

	def __repr__(self):
		return "<Stack('%i','%i')>" % (self.id, self.location)

	def size(self):
		return len(self.characters) + len(self.units)

	def side(self):
		return self.characters[0].side

	def spaceship(self):
		for character in self.characters:
			for possession in character.possessions:
				if possession.type == 'spaceship':
					return possession
		return None

	def stack_detection(self):                  #Check if any characters in the
		for character in self.characters:       #stack are detected.
			if character.detected == True:
				return True
		return None
	# function to add unit to stack, check if not already in another stack, if so, remove?

	def find_stack_leader(self):    #stack leader will be the character with
		leadership_rating = 0       #the highest leadership rating
		for character in self.characters:
			if character.leadership > leadership_rating:
				leadership_rating = character.leadership
		return leadership_rating

	def is_rebel_stack(self):
		for militaryunit in self.militaryunits:
			if militaryunit.side == 'Rebel':
				return True
			else:
				return False

	#trouble referencing the environ type that the stack is in.
	#def check_rebel_environ(self):
	#    for militaryunit in self.militaryunits:
	#        if(militaryunit.type == self.environs.type):
	 #           print "Military unit type and environ type match!"
	  #          return True
	   #     else:
		#        print "Military units are not in their home environ type :("
		 #       return False

Base.metadata.create_all(engine)

