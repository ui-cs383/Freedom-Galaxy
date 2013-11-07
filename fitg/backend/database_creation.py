#Author: Greg Donaldson
#Purpose: Created for the purpose of pulling data from the .dat files for Freedom in the Galaxy. 
#Primarily for use by the backend team. This will allow for a database to be used.

#os is needed to make sure we don't connect to a pre-existing database.
#The others are for creating the database.

import os
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dataSnag import *

def loadDatabase ():

    #These are the lists returned by dataSnag's functions. Necessary for the database.

    actionList = commaWithSpace("action.dat")
    #arc.dat: Needed for Province Game
    #backdoor.dat: Scenario
    ccList = commaOnly("cc_tab.dat")
    charList = commaOnly("charactr.dat")
    detectList = commaOnly("detect.dat")
    #distance.dat: Needed for Province Game
    #egrix.dat: Scenario
    environList = commaOnly("environ.dat")
    #galactic.dat: Scenario
    #galevent.dat: Needed for Galactic Game
    #guistar.dat: Scenario file. Necessary?
    #helsinki.dat: Scenario
    #lookup.dat: Needed for Galactic Game.
    milCombatList = commaOnly("milcomb.dat")
    #orlog.dat: Scenario
    #path.dat: Need key, no idea.
    planetList = commaOnly("planet.dat")
    possessionList = commaWithSpace("possessn.dat")
    #possimg.dat: Discuss. Need to be stored for Client?
    raceList = raceSnag("races.dat")
    #sov_hnd.dat: Need key, not star system, used by Environ
    spaceshipList = commaOnly("spacship.dat")
    #strategy.dat: Galactic Game
    #varu.dat: Scenario

    #Alright, time to check if the database already exists. If it does, get rid of it. 
    #If it doesn't, don't.
    
    try:
        os.remove("Freedom.db")
        db = create_engine('sqlite:///Freedom.db')
    except:      
        db = create_engine('sqlite:///Freedom.db')    
    
    Base = declarative_base()           #Alright, set up the database.
    Session = sessionmaker(bind=db)     #Create a Session, binding it to the database.
    session = Session()                 #Instantiate the database.

    #Each class of the database is one of the tables inside of it.
    
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
            
        #This is the function that is called when an instance of this class
        # is asked to 'repr'esent itself, ie. print AnInstance will print the returned string
        
        def __repr__(self):
            return "<Action('%s','%s', '%s')>" % (self.cardNumber, 
                    self.firstOpt, self.secondOpt, self.thirdOpt)

    class charCombat(Base):
        __tablename__ = 'charCombat'
        dice = Column(Integer, primary_key=True)    #This simulates the character combat table. Dice is the row, where each column is the difference in modifiers.
        neg7orless = Column(String)                 #-7 or less column.
        neg6toneg4 = Column(String)                 #-6 to -4 column.
        neg3toneg2 = Column(String)                 #-3 to -2 column.
        negone = Column(String)                     #-1 column
        zero = Column(String)                       # 0 column
        one = Column(String)                        # 1 column
        twoto3 = Column(String)                     # 2 to 3 column.
        fourto6 = Column(String)                    # 4 to 6 column.
        sevento10 = Column(String)                  # 7 to 10 column.
        elevenormore = Column(String)               # 11 or more column.
        
        def __init__(self, dice, neg7orless, neg6toneg4, neg3toneg2, negone, 
                    zero, one, twoto3, fourto6, sevento10, elevenormore) :
            self.dice = dice
            self.neg7orless = neg7orless
            self.neg6toneg4 = neg6toneg4
            self.neg3toneg2 = neg3toneg2
            self.negone = negone
            self.zero = zero
            self.one = one
            self.twoto3 = twoto3
            self.fourto6 = fourto6
            self.sevento10 = sevento10
            self.elevenormore = elevenormore
            
        def __repr__(self):
            return "<charCombat('%s','%s', '%s')>" % (self.dice, self.neg7orless, 
                    self.neg6toneg4, self.neg3toneg2, self.negone, self.zero, 
                    self.one, self.twoto3, self.fourto6, self.sevento10, self.elevenormore)

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
            
        def __repr__(self):
            return "<Character('%s','%s', '%s')>" % (self.name, self.gif, 
                    self.title, self.location, self.side, self.combat, 
                    self.endurance, self.intelligence, self.leadership, 
                    self.diplomacy, self.navigation, self.homeworld, self.bonuses, 
                    self.wounds, self.detected, self.possession)                        
            
    class Detection(Base):
        __tablename__ = 'detection'
        dice = Column(Integer, primary_key=True)    #This simulates the Detection table. Dice is the row, where each column is the evasion statistic.
        zero = Column(String)
        one = Column(String)
        two = Column(String)
        three = Column(String)
        four = Column(String)
        fiveor6 = Column(String)
        sevenor8 = Column(String)
        nineormore = Column(String)
        
        def __init__(self, dice, zero, one, two, three, 
                    four, fiveor6, sevenor8, nineormore) :
            self.dice = dice
            self.zero = zero
            self.one = one
            self.two = two
            self.three = three
            self.four = four
            self.fiveor6 = fiveor6
            self.sevenor8 = sevenor8
            self.nineormore = nineormore
            
        def __repr__(self):
            return "<Detection('%s','%s', '%s')>" % (self.dice, self.zero, 
                    self.one, self.two, self.three, self.four, 
                    self.fiveor6, self.sevenor8, self.nineormore)
                    
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
            return "<Environ('%s','%s', '%s')>" % (self.id, self.type, self.size, 
					self.race, self.starfaring, self.resources, 
					self.starresources, self.monster, self.coup, self.sov)   
            
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
            
    Base.metadata.create_all(db)    #Create the database.
  
    i = 1
    
    #The following for loops load up the database with relevant info pulled from the .dat files.
    
    for list in actionList:
        temp = Action(i, list[0], list[1], list[2])
        session.add(temp)
        i += 1
    i = 1
    session.commit()
    
    for list in ccList:
        temp = charCombat(i, list[0], list[1], list[2], list[3], list[4], 
                          list[5], list[6], list[7], list[8], list[9])
        session.add(temp)
        i += 1
    i = 1
    session.commit()
    
    for list in charList:
        temp = Character(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], 
                          list[8], list[9], list[10], list[11], list[12], 0, False, False)
        session.add(temp)
    session.commit()
    
    for list in detectList:
        temp = Detection(i, list[0], list[1], list[2], list[3], list[4], 
                         list[5], list[6], list[7])
        session.add(temp)
        i += 1
    session.commit()
    
    for list in environList:
        if list[8] > 3:
            temp = Environ(list[0], list[1], list[2], list[3], list[4], 
                           list[5], list[6], list[7], -1, list[8])
        else:
            temp = Environ(list[0], list[1], list[2], list[3], list[4], 
                           list[5], list[6], list[7], list[8], -1)
        session.add(temp)
    session.commit()
    i = 1
    
    for list in milCombatList:
        temp = milCombat(i, list[0], list[1], list[2], list[3], list[4], 
                         list[5], list[6], list[7], list[8], list[9], list[10])
        session.add(temp)
        i += 1
    session.commit()
    
    for list in planetList:
        temp = Planet(list[0], list[1], list[2], list[3], list[4], list[5])
        session.add(temp)
    session.commit()
    
    for list in possessionList:
        if len(list) == 2:
            continue
        elif len(list) == 4:
            temp = Possession(list[0], list[1], list[2], list[3], " ", " ", " ", " ", False)
        elif len(list) == 5:
            temp = Possession(list[0], list[1], list[2], list[3], list[4], " ", " ", " ", False)
        elif len(list) == 6:
            temp = Possession(list[0], list[1], list[2], list[3], list[4], list[5], " ", " ", False)
        elif len(list) == 7:
            temp = Possession(list[0], list[1], list[2], list[3], list[4], list[5], list[6], " ", False)
        session.add(temp)
        
    for list in spaceshipList:
        if list[7] == "null":
            temp = Possession(list[0], list[1], list[2], list[3], list[4], list[5], list[6], " ", False)
        else:
            temp = Possession(list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], False)
        session.add(temp)
    session.commit()

    for list in raceList:
        if list[4] == '*':
            temp = Race(list[0], list[1], list[2], list[3], False)
        else:
            temp = Race(list[0], list[1], list[2], list[3], True)
        session.add(temp)
    session.commit()

loadDatabase()