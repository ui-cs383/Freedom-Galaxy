#Author: Jeff Crocker
#Purpose: The Object Relational Mapping to the Freedom.db


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

    #Initialize the class.
    
    def __init__(self, cardNumber, firstOpt, secondOpt, thirdOpt):
        self.cardNumber = cardNumber
        self.firstOpt = firstOpt
        self.secondOpt = secondOpt
        self.thirdOpt = thirdOpt
    
    def __repr__(self):
        return "<Action('%s')>" % (self.cardNumber)
        

class Character(Base):
    __tablename__ = 'characters'
    name = Column(String, primary_key=True)     #Name of the character.
    gif = Column(String)                        #Character's associated gif.
    title = Column(String)                      #Character's title, if any.
    location = Column(String)                   #Character's location.
    side = Column(String)                       #Character's side
    combat = Column(Integer)                    #Combat stat
    endurance = Column(Integer)                 #Endurance stat
    intelligence = Column(Integer)              #Intelligence stat
    leadership = Column(Integer)                #Leadership stat
    diplomacy = Column(Integer)                 #Diplomacy stat
    navigation = Column(Integer)                #Navigation stat
    homeworld = Column(String)                  #Homeworld stat
    bonuses = Column(String)                    #Character's bonuses (Usually associated with bonus draws.
    wounds = Column(Integer)                    #Number of character's wounds.
    detected = Column(Boolean)                  #Whether or not the character is detected.
    possession = Column(Boolean)                #What the character has in their possession.
    active = Column(Boolean)
    captive = Column(Boolean)
    stack_id = Column(Integer, ForeignKey('stacks.id'))
    stack = relationship("Stack", backref=backref('characters', order_by=combat))
    
    def __init__(self, name, gif, title, location, side, 
                combat, endurance, intelligence, leadership, diplomacy, 
                navigation, homeworld, bonuses, wounds, detected, possession) :
        self.name = name
        self.gif = gif
        self.title = title
        self.location = location
        self.side = side
        self.combat = combat
        self.endurance = endurance
        self.intelligence = intelligence
        self.leadership = leadership
        self.diplomacy = diplomacy
        self.navigation = navigation
        self.homeworld = homeworld
        self.bonuses = bonuses
        self.wounds = wounds
        self.detected = detected
        self.possession = possession
        self.active = True
        self.captive = False
        
    def __repr__(self):
        return "<Character('%s','%s', '%s')>" % (self.name, self.title, self.location)                        

                
class Environ(Base):
    __tablename__ = 'environs'
    id = Column(String, primary_key=True)   #The environ id. First three characters refer to the planet, last character is the order of the environ (first, second, etc)
    type = Column(String)                   #Environ type
    size = Column(Integer)                  #Environ size
    race = Column(String)                   #Native race to the environ
    starfaring = Column(Integer)            #Whether that race is starfaring (1 is yes, 0 is no)
    resources = Column(Integer)             #Amount of resources available.
    starresources = Column(Integer)         #Whether those resources are starfaring (1 is yes, 0 is no)
    monster = Column(String)                #What race of monster, if any.
    coup = Column(Integer)                  #Coup rating. -1 if no coup rating.
    sov = Column(Integer)                   #Soveriegn number. -1 if no soveriegn present.
    
    def __init__(self, id, type, size, race, starfaring, resources, 
                starresources, monster, coup, sov) :
        self.id = id
        self.type = type
        self.size = size
        self.race = race
        self.starfaring = starfaring
        self.resources = resources
        self.starresources = starresources
        self.monster = monster
        self.coup = coup
        self.sov = sov
      
    def __repr__(self):
        return "<Environ('%s','%s', '%s')>" % (self.id, self.type, self.size)
        
class milCombat(Base):
    __tablename__ = 'milCombat'
    dice = Column(Integer, primary_key=True)    #This simulates the military combat table. Dice is the row, where each column is the odds.
    oneto6 = Column(String)
    oneto5 = Column(String)
    oneto4 = Column(String)
    oneto3 = Column(String)
    oneto2 = Column(String)
    oneto1 = Column(String)
    twoto1 = Column(String)
    threeto1 = Column(String)
    fourto1 = Column(String)
    fiveto1 = Column(String)
    sixto1 = Column(String)
    
    def __init__(self, dice, oneto6, oneto5, oneto4, oneto3, 
                oneto2, oneto1, twoto1, threeto1, fourto1, fiveto1, sixto1) :
        self.dice = dice
        self.oneto6 = oneto6
        self.oneto5 = oneto5
        self.oneto4 = oneto4
        self.oneto3 = oneto3
        self.oneto2 = oneto2
        self.oneto1 = oneto1
        self.twoto1 = twoto1
        self.threeto1 = threeto1
        self.fourto1 = fourto1
        self.fiveto1 = fiveto1
        self.fiveto1 = fiveto1
        self.sixto1 = sixto1
        
    def __repr__(self):
        return "<milCombat('%s','%s', '%s')>" % (self.dice, self.oneto6, 
                self.oneto5, self.oneto4, self.oneto3, self.oneto2, self.oneto1, 
                self.twoto1, self.threeto1, self.fourto1, self.fiveto1, self.sixto1)
                
class Planet(Base):
    __tablename__ = 'planets'
    id = Column(Integer)                        #Planet id.
    name = Column(String, primary_key=True)     #Planet name.
    race = Column(String)                       #Native race to the planet, if any.
    sloyalty = Column(Integer)                  #Loyalty value for one variant of the game.
    aloyalty = Column(Integer)                  #Loyalty value for another variant of the game.
    numEnvirons = Column(Integer)               #Number of environs this planet has.

    def __init__(self, id, name, race, sloyalty, aloyalty, numEnvirons):
        self.id = id
        self.name = name
        self.race = race
        self.sloyalty = sloyalty
        self.aloyalty = aloyalty
        self.numEnvirons = numEnvirons
        
    def __repr__(self):
        return "<Planet('%s','%s', '%s')>" % (self.id, self.race, 
                self.sloyalty, self.aloyalty, self.numEnvirons)
                
class Possession(Base):
    __tablename__ = 'possessions'
    type = Column(String)                   #Type of possession.
    name = Column(String, primary_key=True) #Name of possession.
    gif = Column(String)                    #gif related to the possession.
    stat1 = Column(String)                  #First stat.
    stat2 = Column(String)                  #Second stat.
    stat3 = Column(String)                  #Third stat.
    stat4 = Column(String)                  #Fourth stat.
    owner = Column(String)                  #Possession's owner.
    damaged = Column(Boolean)               #Whether the possession is damaged. This really only applies to starships.
    
    def __init__(self, type, name, gif, stat1, stat2, 
                stat3, stat4, owner, damaged) :
        self.type = type
        self.name = name
        self.gif = gif
        self.stat1 = stat1
        self.stat2 = stat2
        self.stat3 = stat3
        self.stat4 = stat4
        self.owner = owner
        self.damaged = damaged
        
    def __repr__(self):
        return "<Possession('%s','%s', '%s')>" % (self.type, self.name, 
                self.gif, self.stat1, self.stat2, self.stat3, 
                self.stat4, self.owner, self.damaged)
                
class Race(Base):
    __tablename__ = 'races'
    name = Column(String, primary_key=True) #Races name.
    environ = Column(String)                #Environ they might be found in.
    combat = Column(Integer)                #Combat stat
    endurance = Column(Integer)             #Endurance stat
    firefight = Column(Boolean)             #Whether or not engaging this race is a firefight.

    def __init__(self, name, environ, combat, endurance, firefight):
        self.name = name
        self.environ = environ
        self.combat = combat
        self.endurance = endurance
        self.firefight = firefight
        
    def __repr__(self):
        return "<Race('%s','%s', '%s')>" % (self.name, self.environ, 
                self.combat, self.endurance, self.firefight)
        
class Stack(Base):
    __tablename__ = 'stacks'

    id = Column(Integer, primary_key=True)
    location = Column(String(40))

    def __init__(self, id, location):
        self.id = id
        self.location = location

    # function to add unit to stack, check if not already in another stack, if so, remove?