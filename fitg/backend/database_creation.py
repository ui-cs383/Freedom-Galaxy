from sqlalchemy import *
from dataSnag import *

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
#sov_hnd.dat: Need key, not star system
spaceshipList = commaOnly("spacship.dat")
#strategy.dat: Galactic Game
#varu.dat: Scenario

dictList = []
db = create_engine('sqlite://')

metadata = MetaData(db)

Action = Table('Action', metadata,
    Column('cardNumber', Integer, primary_key=True),
    Column('firstOpt', String(40)),
    Column('secondOpt', String(40)),
    Column('thirdOpt', String(40))
)

charCombat = Table('charCombat', metadata,
    Column('dice', Integer, primary_key=True),
    Column('neg7orless', String(40)),
    Column('neg6toneg4', String(40)),
    Column('neg3toneg2', String(40)),
    Column('negone', String(40)),
    Column('zero', String(40)),
    Column('one', String(40)),
    Column('2to3', String(40)),
    Column('4to6', String(40)),
    Column('7to10', String(40)),
    Column('11ormore', String(40))
)

Characters = Table('Characters', metadata,
    Column('name', String(40), primary_key=True),
    Column('gif', String(40)),
    Column('title', String(40)),
    Column('location', String(40)),
    Column('side', String(40)),
    Column('combat', Integer),
    Column('endurance', Integer),
    Column('intelligence', Integer),
    Column('leadership', Integer),
    Column('diplomacy', Integer),
    Column('navigation', Integer),
    Column('homeworld', String(40)),
    Column('bonuses', String(40)),
    Column('wounds', Integer)
)

Detection = Table('Detection', metadata,
    Column('dice', String(40), primary_key=True),
    Column('zero', String(40)),
    Column('one', String(40)),
    Column('two', String(40)),
    Column('three', String(40)),
    Column('four', String(40)),
    Column('5or6', String(40)),
    Column('7or8', String(40)),
    Column('9ormore', String(40))
)

Environ = Table('Environ', metadata,
    Column('id', Integer, primary_key=True),
    Column('type', String(40)),
    Column('size', Integer),
    Column('race', Integer),
    Column('starfaring', Boolean),
    Column('resources', Integer),
    Column('',Integer),
    Column('monster', String(40)),
    Column('', Integer)
)

milCombat = Table('milCombat', metadata,
    Column('dice', String(40), primary_key=True),
    Column('1to6', String(40)),
    Column('1to5', String(40)),
    Column('1to4', String(40)),
    Column('1to3', String(40)),
    Column('1to2', String(40)),
    Column('1to1', String(40)),
    Column('2to1', String(40)),
    Column('3to1', String(40)),
    Column('4to1', String(40)),
    Column('5to1', String(40)),
    Column('6to1', String(40))  
)

Planets = Table('Planets', metadata,
    Column('id', Integer),
    Column('name', String(40), primary_key=True),
    Column('race', String(40)),
    Column('sloyalty', Integer),
    Column('aloyalty', Integer),
    Column('numenvirons', Integer)
)

Possessions = Table('Possessions', metadata,
    Column('type', String(40)),
    Column('name', String(40), primary_key=True),
    Column('gif', String(40)),
    Column('stat1', String(40)),
    Column('stat2', String(40)),
    Column('stat3', String(40)),
    Column('stat4', String(40)),
    Column('owner', String(40)),
    Column('damaged', Boolean)
)

Races = Table('Races', metadata,
    Column('name', String(40), primary_key=True),
    Column('environ', String(40)),
    Column('combat', String(40)),
    Column('endurance', String(40)),
    Column('firefight', Boolean)
)

metadata.create_all()
conn = db.connect()

i = 1

for list in actionList:
    temp = {'cardNumber' : i, 'firstOpt' : list[0], 'secondOpt' : list[1], 'thirdOpt' : list[2]}
    dictList.append(temp)
    i += 1
conn.execute(Action.insert(), dictList)
dictList = []   
i = 1
    
for list in ccList:
    temp = {'dice' : i, 'neg7orless' : list[0], 'neg6toneg4' : list[1], 'neg3toneg2' : list[2], 
            'negone' : list[3], 'zero' : list[4], 'one' : list[5], '2to3' : list[6], 
            '4to6' : list[7], '7to10' : list[8], '11ormore': list[9]}
    i += 1
conn.execute(charCombat.insert(), dictList)
dictList = []
    
for list in charList:
    temp = {'name' : list[0], 'gif' : list[1], 'title' : list[2], 'location' : list[3], 
            'side' : list[4], 'combat' : list[5], 'endurance' : list[6], 'intelligence' : list[7], 
            'leadership' : list[8], 'diplomacy' : list[9], 'navigation' : list[10], 
            'homeworld' : list[11], 'bonuses' : list[12], 'wounds' : 0}
    dictList.append(temp)
conn.execute(Characters.insert(), dictList)
dictList = []
i = 1

for list in detectList:
    temp = {'dice' : i, 'zero' : list[0], 'one' : list[1], 'two' : list[2], 'three' : list[3], 
            'four' : list[4], '5or6' : list[5], '7or8' : list[6], '9ormore' : list[7]}
    dictList.append(temp)
    i += 1
conn.execute(Detection.insert(), dictList)
dictList = []
i = 1

for list in milCombatList:
    temp = {'dice' : i, '1to6' : list[0], '1to5' : list[1], '1to4' : list[2], '1to3' : list[3], 
            '1to2' : list[4], '1to1' : list[5], '2to1' : list[6], '3to1' : list[7], '4to1' : list[8],
            '5to1' : list[9], '6to1' : list[10]}
    dictList.append(temp)
    i += 1
conn.execute(milCombat.insert(), dictList)
dictList = []

for list in planetList:
    temp = {'id' : list[0], 'name' : list[1], 'race' : list[2], 
            'sloyalty' : list[3], 'aloyalty' : list[4], 'numenvirons' : list[5]}
    dictList.append(temp)
conn.execute(Planets.insert(), dictList)
dictList = []

for list in possessionList:
    if len(list) == 2:
        continue
    elif len(list) == 4:
        temp = {'type' : list[0], 'name' : list[1], 'gif' : list[2], 'stat1' : list[3], 
                'stat2' : "", 'stat3' : "", 'stat4' : "", 'owner' : "", 'damaged' : False}
    elif len(list) == 5:
        temp = {'type' : list[0], 'name' : list[1], 'gif' : list[2], 'stat1' : list[3], 
                'stat2' : list[4], 'stat3' : "", 'stat4' : "", 'owner' : "", 'damaged' : False}
    elif len(list) == 6:
        temp = {'type' : list[0], 'name' : list[1], 'gif' : list[2], 'stat1' : list[3], 
                'stat2' : list[4], 'stat3' : list[5], 'stat4' : "", 'owner' : "", 'damaged' : False}
    elif len(list) == 7:
        temp = {'type' : list[0], 'name' : list[1], 'gif' : list[2], 'stat1' : list[3], 
                'stat2' : list[4], 'stat3' : list[5], 'stat4' : list[6], 'owner' : "", 'damaged' : False}
    dictList.append(temp)
    
for list in spaceshipList:
    if list[7] == "null":
        temp = {'type' : list[0], 'name' : list[1], 'gif' : list[2], 'stat1' : list[3], 
                'stat2' : list[4], 'stat3' : list[5], 'stat4' : list[6], 'owner' : "", 'damaged' : False}
    else:
        temp = {'type' : list[0], 'name' : list[1], 'gif' : list[2], 'stat1' : list[3], 
                'stat2' : list[4], 'stat3' : list[5], 'stat4' : list[6], 'owner' : list[7], 'damaged' : False}
    dictList.append(temp)
conn.execute(Possessions.insert(), dictList)
dictList = []

for list in raceList:
    if list[4] == '*':
        temp = {'name' : list[0], 'environ' : list[1], 'combat' : list[2], 
                'endurance' : list[3], 'firefight' : False}
    else:
        temp = {'name' : list[0], 'environ' : list[1], 'combat' : list[2], 
                'endurance' : list[3], 'firefight' : True}
    dictList.append(temp)
conn.execute(Races.insert(), dictList)
dictList = []

"""for row in conn.execute(select([Planets])):
    print row"""
