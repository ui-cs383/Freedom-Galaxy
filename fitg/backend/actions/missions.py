# Author: Jeff Crocker

from orm import *
from combat import *
from random import randint

def assign_mission(session, stack_id, mission_type):
    mission = session.query(Mission).filter_by(type = mission_type).one()
    session.add(mission)
    if mission.stack == None:
        mission.stack_id = stack_id
        session.commit()
        return True, mission.__dict__
    else:
        return False, mission.__dict__
    
def attempt_mission(session, environ_id):
    environ = session.query(Environ).filter_by(id = environ_id).one()
    for stack in environ.stacks:
        for mission in stack.mission:
            successes = 0
            for x in range(environ.size): """+ (mission.draws)()"""
                if draw_action(mission, environ, session) == mission.type:
                    successes += 1
                    #   Do mission result
            return resolve_mission(session, mission, successes)

def resolve_mission(session, mission, successes):
    session.add(mission)
    mission_table = {
        'A' : a_mission,
        'B' : b_mission,
        'C' : c_mission,
        'D' : d_mission,
        'F' : f_mission,
        'G' : g_mission,
        'I' : i_mission,
        'P' : p_mission,
        'R' : r_mission,
        'S' : s_mission,
        'T' : t_mission
    }
    result = mission_table['mission.type'](session, mission, successes)
    session.commit()

    return True, result

def a_mission(session, mission, successes):
    if successes > 0:
        target_stacks = session.query(Stack).filter_by(environ = mission.environ).all()
        for stack in target_stacks:
            if stack.side() != mission.stack.side():
                if stack.characters:
                    victim = stack.characters[randint(0,stack.size()-1)]
                    session.delete(victim)
                    session.commit()
                    return stack.__dict__

def b_mission(session, mission, successes):
    pass

def c_mission(session, mission, successes):
    pass

def d_mission(session, mission, successes):
    mission.environ.planet

def f_mission(session, mission, successes):
    pass

def g_mission(session, mission, successes):
    pass

def i_mission(session, mission, successes):
    pass

def p_mission(session, mission, successes):
    pass

def r_mission(session, mission, successes):
    if mission.stack.side() == 'Rebel':
        if successes > 0:
            mission.environ.planet.in_rebellion = True
    elif mission.stack.side() == 'Imperial':
        if successes > 1:
            mission.environ.planet.in_rebellion = False

def s_mission(session, mission, successes):
    if successes >= 2:
        mission.environ.planet.pdb_change(-1)
    if successes >= 1:
        mission.environ.planet.pdb_state = 0

def t_mission(session, mission, successes):
    pass


def draw_action(mission, environ, session):
    action_table = (
        (('RH',CAoNA),('B',LR),('P',LSC)),(('D',CAoR),('CS',WD),('PI',CMA1aCD)),
        (('PI',CAoR),('SC',CD),('RG',LR)),(('CJ',ILA),('BT',RCOaCD),('PG',WD)),
        (('PG',ILA),('C',CPM),('DH',CAPaGGO)),(('D',RCOaCD),('GI',WD),('RS',WSC)),
        (('P',ERMaCD),('BH',ILA),('C',CAoNA)),(('FG',CD),('D',PGW),('AH',CAoR)),
        (('A',LSC),('BE',CAoR),('FB',CMA2aCD)),(('C',WD),('SE',CMA3aCD),('FI',LEM)),
        (('CS',LEM),('DG',CMA4aCD),('FP',CDRaNBD)),(('SH',LEM),('GP',CAoR),('B',CW)),
        (('RE',LEM),('FP',CL),('CS',MGS)),(('FI',WSC),('CT',AWH),('E',CPM)),
        (('G',CW),('RS',WD),('D',PGW)),(('DS',LR),('RQ',CDaCS),('F',RCOaCD)),
        (('FP',LR),('R',CAoR),('SH',CD)),(('GI',PGW),('R',CDaCS),('SE',CAoR)),
        (('FI',CDaCS),('AJ',CDRaNBD),('CT',CDaCS)),(('SC',DFSaNBD),('R',CMA5aCD),('FG',CDaCS)),
        (('T',CDRaNBD),('F',MGS),('BJ',WD)),(('CE',CAPaAGO),('P',CW),('R',LEM)),
        (('B',CL),('CH',ERMaCD),('GI',CL)),(('BE',CPM),('P',LEM),('RQ',ILA)),
        (('SG',CMA4aCD),('FI',LEM),('RT',nCA)),(('RB',CMA5aCD),('F',CAPaGGO),('SC',CL)),
        (('DQ',CMA6aCD),('FG',DFSaNBD),('BE',PGW)),(('RH',CDaCS),('FI',PGW),('B',CAoR)),
        (('AT',CDaCS),('DE',WSC),('P',DFSaNBD)),(('F',PGW),('SH',CAoNA),('D',ERMaCD))
    )

    if environ.type == 'U':
        result = action_table[randint(0,29)][0]
    elif environ.type == 'W':
        result = action_table[randint(0,29)][2]
    else:
        result = action_table[randint(0,29)][1]

    result[1](mission, session)

#  AWH:     Accidents Will Happen
#       (especially in an unfamiliar environ.  Any one character
#       performing a mission in the environ must receive a wound.) 
def AWH(mission, session):
    for character in mission.stack.characters:
        character.wounds += 1
        if character.wounds >= character.endurance:
            session.delete(character)
            session.commit()
            if mission.stack.size() == 0:
                session.delete(mission.stack)
                session.delete(mission)
    session.commit()


#  CAoNA:   Creature Attacks or No Action                            
#       (if a creature is not named in the environ ignore event)     
#                                               
def CAoNA(mission, session):
    # need to implement creature look-up function? lots of special cases....
    #creature = mission.stack.location.monster
    creature = ("Sentry Robot",4,2)
    new_char = Character("Sentry Robot", '', '', '', "Creature", 4, 2, 1, 1, 1, '', '', '')
    session.add(new_char)
    new_stack = Stack()
    session.add(new_stack)
    new_stack.characters.append(new_char)
    session.commit()
    combat_round = 1
    while session.query(Stack).filter_by(id = new_stack.id).first():
        combat_round += 1
        char_combat(new_stack.id, mission.stack.id, "")
    session.delete(new_stack)
    session.commit()

    
                         
#  CAoxR:   Creature Attacks or One Sentry Robot                     
#       (if a creature is named in the environ, look it up in the    
#       Galatic guide to determine its attributes.  If no creature   
#       is named, the mission group is attacked by x (x will be 1    
#               or 2) sentry robot.)                                 
#                                       
def CAoR(mission, session):
    CAoNA(mission, session)                           
#  CAPaAGO: Commit Atrocity Planet and Advanced Game Only            
#       (otherwise ignore event)                                     
#                                     
def CAPaAGO(mission, session):
    pass                               
#  CAPaGGO: Commit Attrocity Planet and Galatic Game Only            
#       (the imperial player may commit an atrocity on this planet.  
#       Galatic Game only, otherwise ignore event.)                  
#                                   
def CAPaGGO(mission, session):
    pass                                 
#  CD:      Characters Detected                                      
#                              
def CD(mission, session):
    for character in mission.stack.characters:
        session.add(character)
        character.detected = True
        # run combat ?
    session.commit()

#  CDaCS:   Characters Detected and Conduct Search                   
#       (Enemy player may conduct search for one mission group       
#       in environ.)                                                 
#                            
def CDaCS(mission, session):
    CD(mission, session)
    # conduct search                                        
#  CDRaNBD: Characters Delayed Rumors and No Bonus Draws             
#       (may be taken in this Environ this Mission Phase.)           
#                 
def CDRaNBD(mission, session):

#  CL:      Confusing Local                                          
#       (protocal aborts a diplomacy mission.  If one is being       
#       performed in the Environ, shift the Loyalty marker one       
#       space in the Non-Phasing Player's favor.)                    
#                   
def CL(mission, session):
    if mission.type == 'D':
        mission.stack = None
        session.add(mission)
        session.commit()                                                
#  CMA1aCD: Coup Mission Aborted 1 and Characters Detected           
#       (Type 1: Roll the die. 1-3 no effect; 4 shift loyalty        
#       marker one space in non phasing player's favor; 5 or 6       
#       shift loyalty and entire Missions group captured.)        #
#                 
def CMA1aCD(mission, session):
    session.add(mission)
    rand = randint(1,6)
    if rand > 3:
        mission.environ.loyalty += 1
    if mission.type == 'C':
        mission.stack = None

    session.commit()
    CD(mission, session)                                                  
#  CMA2aCD: Coup Mission Aborted 2 and Characters Detected           
#       (Type 2.  Roll the die 1-4, no effect; 5, shift loyalty      
#       marker one space in non phasing player's favor; 6, shift     
#       Loyalty and entire mission group captured.)                  
#                
def CMA2aCD(mission, session):
    CMA1aCD(mission, session)                                                    
#  CMA3aCD: Coup Mission Aborted 3 and Characters Detected           
#       (Type 3.  Roll the die 1, 2, no effect; 3-5, shift loyalty   
#       marker one space in non phasing player's favor; 5, 6 shift   
#       Loyalty and Mission group captured, one character killed.    
#       (Phasing Player's Choice))                                   
#              
def CMA3aCD(mission, session):
    CMA1aCD(mission, session)                                                      
#  CMA4aCD: Coup Mission Aborted 4 and Characters Detected           
#       (Type 4.  Roll the die 1-3 no effect; 4,5, shift loyalty     
#       marker one space in non-Phasing Player's favor; 6, shift     
#       Loyalty and entire Mission Group Killed.)                    
#             
def CMA4aCD(mission, session):
    CMA1aCD(mission, session)                                                       
#  CMA5aCD: Coup Mission Aborted 5 and Characters Detected           
#       (Type 5.  Roll the die 1, 2, no effect; 3, 4, shift          
#       loyalty marker one space in non phasing player's favor;      
#       5, 6, shift Loyalty and mission group found by Enemy squad   
#       or characters. (Non Phasing Players Choice.)                 
#              
def CMA5aCD(mission, session):
    CMA1aCD(mission, session)                                                      
#  CMA6aCD: Coup Mission Aborted 6 and Characters Detected           
#       (Type 6.  Roll the die.  1-3, shift loyalty marker one       
#       space in Non-Phasing Players favor; 4-6 shift Loyalty and    
#       Mission Group found by Enemy Squad or characters. (Non-      
#       Phasing Players Choice))                                     
#             
def CMA6aCD(mission, session):
    CMA1aCD(mission, session)                                                       
#  CPM:     Controversial Political Matters                          
#       (argued.  If a Diplomacy mission is being performed, and     
#       no character in the Mission Group has a Diplomacy Rating     
#       of two or more, the mission is aborted.)                     
#               
def CPM(mission, session):
    session.add(mission)
    if mission.type == 'D':
        for character in mission.stack.characters:
            if characters.diplomacy >= 2:
                return

    mission.stack = None
    session.commit()                                            
#  CW:      Civil War                                                
#       (breaks out.  The populace blames the phasing player.  If    
#       the loyalty marker is currently at 1 or 2 in the player's    
#       favor, move the marker to Neutral.  If the Planet is in      
#       rebellion or not in the player's favor, ignore event.)       
#               
def CW(mission, session):
    pass
#  DFSaNBD: Disagreeble Food Substance and No Bonus Draws            
#       (hampers characters, and no bonus draws may be taken in      
#       this environ this mission phase.)                            
#               
def DFSaNBD(mission, session):
    pass
#  ERMaCD:  Enemy Reveals Mission and Characters Detected            
#       (The non phasing player randomly chooses one mission         
#       that the phasing player is currently performing in the       
#       environ; that mission is aborted.)                           
#                
def ERMaCD(mission, session):
    CD(mission, session)                                                    
#  ILA:     Irate Locals Attack                                      
#       (one mission group. Refer to the irate locals chart to       
#       determine the mob's attributes.)                             
#               
def ILA(mission, session):
    pass                                                     
#  LEM:     Local Expidite Missions                                  
#       (local connections expedite missions.  All missions receive  
#       one extra bonus draw in this environ in this mission phase.) 
#        
def LEM(mission, session):
    pass
#  LR:      Locals Raid                                              
#       (enemy forces.  Non phasing player must eliminate one of     
#       his military units in the environ or if he controls a PDB    
#       that is up one the planet, place it down, this is the        
#       non-phasing players choice.)                                 
#             
def LR(mission, session):
    pass                                                       
#  LSC:     Local Shelters Characters                                
#       (from enemy.  No enemy searches may be conducted in this     
#       environ for the remainder of this mission phase.)            
#                
def LSC(mission, session):
    pass                                                    
#  MGS:     Mission Group Stumbles                                   
#       (on enemy squad.  If the enemy player controls the planet    
#       and has military units in the environ character combat is    
#       initiated using the Squad Table to determine the Enemy's     
#       strength.)                                                   
#             
def MGS(mission, session):
    pass                                                       
#  nCA:     not Creature Attacks                                     
#       (It's the off-season for the local creatures.  Ignore all    
#       "Creature Attacks" events in this Environ this Mission       
#       Phase.)                                                      
#            
def nCA(mission, session):
    pass                                                        
#  PGW:     Populace Goes Wild                                       
#       (If the planet is placed into rebellion during this          
#       phase, the Rebel Player receives double the resource         
#       value in this Environ.)                                      
#            
def PGW(mission, session):
    CD(mission, session)                                                        
#  RCOaCD:  Rebels Chicken Out and Characters Detected               
#       (start rebellion mission aborted.)                           
#              
def RCOaCD(mission, session):
    CD(mission, session)                                                      
#  WD:      Weather Disturbances                                     
#       (hamper enemy operations.  The non-Phasing player may        
#       conduct no searches in this environ this mission phase.)     
#              
def WD(mission, session):
    pass                                                      
#  WSC:     Wrong Soldier Contacted                                  
#       (If a subvert toops mission is being performed, it is        
#       aborted Mission group found by enemy squad.  If an enemy     
#       leader is stacked with the enemy military units, the entire  
#       Mission Group is captured.)                                  
#              
def WSC(mission, session):
    pass                                                      

