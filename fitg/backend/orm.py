#Author: Jeff Crocker
#Purpose: The Object Relational Mapping for the Freedom.db


from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

Base = declarative_base()           #Alright, set up the database.
db = create_engine('sqlite:///Freedom.db')
Session = sessionmaker(bind=db)     #Create a Session, binding it to the database.

class Action(Base):
    __tablename__ = 'actions'
    cardNumber = Column(Integer, primary_key=True)  #This is the primary key. Its used to help 'randomly' draw a card.
    firstOpt = Column(String)                       #This is the first option on the card.
    secondOpt = Column(String)                      #This is the second option on the card.
    thirdOpt = Column(String)                       #This is the third option ont he card.

    
    def __init__(self, cardNumber, firstOpt, secondOpt, thirdOpt):
        self.cardNumber = cardNumber
        self.firstOpt = firstOpt
        self.secondOpt = secondOpt
        self.thirdOpt = thirdOpt
    
    def __repr__(self):
        return "<Action('%s','%s')>" % (self.cardNumber, self.firstOpt)
        

class Character(Base):
    __tablename__ = 'characters'
    name = Column(String, primary_key=True)     #Unique name of every character
    gif = Column(String)                        #Does the DB need this?
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
    possession = Column(Boolean)                
    active = Column(Boolean)
    captive = Column(Boolean)
    stack_id = Column(Integer, ForeignKey('stacks.id'))
    stack = relationship("Stack", backref=backref('characters', order_by=combat))
    
    def __init__(self, name, gif, title, race, side, 
                combat, endurance, intelligence, leadership, diplomacy, 
                navigation, homeworld, bonuses) :
        self.name = name
        self.gif = gif
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
    id = Column(String, primary_key=True) 
    type = Column(String)                   
    size = Column(Integer)                  
    starfaring = Column(Integer)            
    resources = Column(Integer)             
    starresources = Column(Integer)         
    monster = Column(String)                
    coup = Column(Integer)                  
    sov = Column(Integer)                   
    planet_id = Column(Integer, ForeignKey('planets.id'))
    planet = relationship("Planet", backref=backref('environs', order_by=id))
    race_name = Column(String, ForeignKey('races.name'))
    race = relationship("Race", backref=backref('environs', order_by=id))      
    
    def __init__(self, id, type, size, race_name, starfaring, resources, 
                starresources, monster, coup, sov, planet_id) :
        self.id = id
        self.type = type
        self.size = size
        self.race_name = race_name
        self.starfaring = starfaring
        self.resources = resources
        self.starresources = starresources
        self.monster = monster
        self.coup = coup
        self.sov = sov
        self.planet_id = planet_id
      
    def __repr__(self):
        return "<Environ('%s','%s', '%s')>" % (self.id, self.type, self.size)

class MilitaryUnit(Base):
    __tablename__ = 'militaryunits'
    id = Column(Integer, primary_key=True)
    type = Column(Integer)    
    side = Column(String)     
    wounds = Column(Integer)  
    stack_id = Column(Integer, ForeignKey('stacks.id'))
    stack = relationship("Stack", backref=backref('militaryunits', order_by=type))
    
    def __init__(self,type,side):
        self.type = type
        self.side = side
        self.wounds = 0

        
    def __repr__(self):
        return "<MilitaryUnit('%s','%s', '%s')>" % (self.id, self.type, self.side)

                
class Planet(Base):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)  
    name = Column(String)                   
    race = Column(String)                   
    loyalty = Column(Integer)               
    numEnvirons = Column(Integer)           

    def __init__(self, id, name, race, loyalty, numEnvirons):
        self.id = id
        self.name = name
        self.race = race
        self.loyalty = loyalty
        self.numEnvirons = numEnvirons
        
    def __repr__(self):
        return "<Planet('%s','%s', '%s')>" % (self.id, self.race, self.numEnvirons)
                
class Possession(Base):
    __tablename__ = 'possessions'
    type = Column(String)                   #Type of possession.
    name = Column(String, primary_key=True) #Name of possession.
    gif = Column(String)                    #gif related to the possession.
    stat1 = Column(String)                  #First stat.
    stat2 = Column(String)                  #Second stat.
    stat3 = Column(String)                  #Third stat.
    stat4 = Column(String)                  #Fourth stat.
    damaged = Column(Boolean)               #Whether the possession is damaged. This really only applies to starships.
    owner_name = Column(String, ForeignKey('characters.name'))
    owner = relationship("Character", backref=backref('possessions', order_by=name))   
    def __init__(self, type, name, gif, stat1, stat2, 
                stat3, stat4, owner_name) :
        self.type = type
        self.name = name
        self.gif = gif
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

    id = Column(Integer, primary_key=True)
    location = Column(Integer)

    def __init__(self, id, location):
        self.id = id
        self.location = location

    def __repr__(self):
        return "<Stack('%i','%i')>" % (self.id, self.location)

    def Size(self):
        return len(self.characters) + len(self.militaryunits)

    # function to add unit to stack, check if not already in another stack, if so, remove?