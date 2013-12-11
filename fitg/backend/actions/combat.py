#from database_creation import loadDatabase
from orm import *
from random import randint
 
#Start Character Combat
#Authored By Jeff Crocker
def char_combat(session, atk_id, def_id, options):

    atk_stack = session.query(Stack).filter_by(id = atk_id).one()
    def_stack = session.query(Stack).filter_by(id = def_id).one()
    session.add(atk_stack, def_stack)

    # still needs to include breakoff


    CD = char_combat_rating(atk_stack, session) - char_combat_rating(def_stack, session)

    if 'C' in options:
        CD -= 2

    atk_result = char_table(randint(0,5),CD,True)
    def_result = char_table(randint(0,5),CD,False)

    if 'F' in options:
        atk_result[0] *= 2
        def_result[0] *= 2

    elif atk_stack.militaryunits:
        atk_result[0] *= 2
        def_result[0] *= 2

    char_wounds(atk_stack, atk_result[0], session)
    char_wounds(def_stack, def_result[0], session)
        
    if 'C' in options:
        if atk_result[1] == 1:
            captured_char = def_stack.characters[randint(0,len(def_stack.characters)-1)]
            captured_char.stack_id = atk_id
            captured_char.captive = True
            captured_char.active = False

        if def_result[1] == 1:
            captured_char = def_stack.characters[randint(0,len(def_stack.characters)-1)]
            captured_char.stack_id = atk_id
            captured_char.captive = True
            captured_char.active = False

    if atk_stack.size() == 0:
        session.delete(atk_stack)

    if def_stack.size() == 0:
        session.delete(def_stack)

def char_combat_rating(StackID, session):
    CR = 0
    # for each character in the stack, sum effective combat strength
    for character in session.query(Stack).filter_by(id = StackID).one().characters:
        if character.active == True:
            CR += character.combat - character.wounds
    return CR

def char_wounds(stack, num_wounds, session):
    # while there are still wounds to assign and characters alive
    while num_wounds > 0 and stack.characters:
        # select random victim from stack
        victim = stack.characters[randint(0,len(stack.characters)-1)]
        session.add(victim)
        victim.wounds += 1
        #print victim.name, " suffers wound!"
        if victim.wounds >= victim.endurance:
            #print victim.name, " has died! :("
            session.delete(victim)
        num_wounds -= 1

    session.commit()

# Simply a direct transfer of character combat table
def char_table(dice, CD, is_attacker):
    attacker_wounds = (
        (4,3,3,2,2,2,2,1,1,1),(4,3,2,2,2,1,1,1,1,0),(3,3,2,2,1,1,1,1,0,0),
        (3,2,2,1,1,1,0,0,0,0),(2,2,1,1,0,0,0,0,0,0),(2,1,0,0,0,0,0,0,0,0))

    defender_wounds = (
        (0,0,0,0,0,0,0,1,1,2),(0,0,0,0,0,0,1,1,1,2),(0,0,0,0,0,1,1,1,2,3),
        (0,0,0,1,1,1,1,2,3,3),(0,0,1,1,1,1,2,2,3,4),(1,1,1,1,2,2,2,3,3,4))

    attacker_capture = (
        (0,0,0,0,0,1,0,0,0,0),(0,0,0,1,1,0,1,1,1,0),(0,1,0,0,0,0,0,0,0,0),
        (0,0,1,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,1,0,0),(0,0,0,0,0,0,0,0,0,0))

    defender_capture = (
        (0,0,0,0,0,0,0,0,1,0),(0,0,0,0,0,0,0,0,0,0),(0,0,0,0,1,0,0,1,1,0),
        (0,0,0,1,0,1,1,1,0,0),(0,0,0,0,0,0,1,0,1,0),(0,0,0,0,0,0,0,0,0,0))

    # A ridiculous way of translating Combat Differentials to appropriate columns
    if CD <= -7:
        CD = 0
    elif CD >= -6 and CD <= -4:
        CD = 1
    elif CD >= -3 and CD <= -2:
        CD = 2
    elif CD == -1:
        CD = 3
    elif CD == 0:
        CD = 4
    elif CD == 1:
        CD = 5
    elif CD >= 2 and CD <= 3:
        CD = 6
    elif CD >= 4 and CD <= 6:
        CD = 7
    elif CD >= 7 and CD <= 10:
        CD = 8
    elif CD >= 11:
        CD = 9

    if is_attacker:
        return (attacker_wounds[dice][CD], attacker_capture[dice][CD])
    else:
        return (defender_wounds[dice][CD], defender_capture[dice][CD])
#End Character Combat

#Start Military Combat
#Authored By Ben Cumber
def mil_combat(session, atk_id, def_id):

    atk_stack = session.query(Stack).filter_by(id = atk_id).one()
    def_stack = session.query(Stack).filter_by(id = def_id).one()

    #atk_mil_units = atk_stack.militaryunits
    #def_mil_units = def_stack.militaryunits
    atk_combat_rating = stack_combat_rating(atk_stack)
    def_combat_rating = stack_combat_rating(def_stack)
    
    #print "Attacker Combat Rating: ", atk_combat_rating
    #print "Defender Combat Rating: ", def_combat_rating

    column = stack_combat_ratio(atk_combat_rating, def_combat_rating)
    column += mil_combat_modifiers(atk_stack, def_stack)

    #print "Column: ", column

    if(column > 10):
        column = 10
    if(column < 0):
        column = 0

    atk_result = mil_combat_table(randint(0,5), column, True)
    def_result = mil_combat_table(randint(0,5), column, False)

    #print "Attackers Eliminated: ", atk_result
    #print "Defenders Eliminated: ", def_result

    #atk_result = mil_combat_table(randint(0, 5), combat_ratio, True)
    #def_result = mil_combat_table(randint(0, 5), combat_ratio, False)

def stack_combat_ratio(atk_rating, def_rating):     #Always round in the
    ratio = 0                                       #defenders favor
    column = 1
    #columns 0 and 10 are only accessible through a modifier shift.

    if(atk_rating > def_rating):#columns 6-9
        ratio =  atk_rating / def_rating
        if(ratio == 1):
            column = 5
        elif(ratio == 2):
            column = 6
        elif(ratio == 3):
            column = 7
        elif(ratio == 4):
            column = 8
        else:
            column = 9
    elif(atk_rating < def_rating):#columns 1-4
        ratio = def_rating / atk_rating
        ratio += 1
        if(ratio >= 5):
            column = 1
        elif(ratio == 4):
            column = 2
        elif(ratio == 3):
            column = 3
        else:
            column = 4
    else:
        #they are equal, the ratio is 1:1, column 5
        column = 5
    return column

def mil_combat_modifiers(atk_obj, def_obj):
    modifier = 0
    atk_leader = atk_obj.find_stack_leader()
    def_leader = def_obj.find_stack_leader()
    leadership = abs(atk_leader - def_leader)
    if(atk_leader > def_leader):
        modifier += leadership
    elif(def_leader > atk_leader):
        modifier -= leadership
    #leadership modifier done

    #now for Rebel unit environ type modifier
    #Step 1:
        #Determine which stack is rebel.
    #Step 2:
        #Determine what type of environ, combat is occuring in.
    #Step 3:
        #Check if rebel units are of same environ type.
    #Step 4:
        #if yes: Shift in their favor.
        #if no: do nothing

#trouble referencing the environ that the stack is in.
#    if atk_obj.is_rebel_stack():
#        if atk_obj.check_rebel_environ():
#            modifier += 1
#    else:
#        if def_obj.check_rebel_environ():
#            modifier -= 1

    #now for special environ modifier (Rebels favor only)
    #occurs only if combat is in liquid, subterranean, air, or fire environ.
    #and only if there is not an imperial leader present.
    #Step 1:
        #Is it a special environ?
    #Step 2:
        #Do the imperials have a leader?
    #Step 3:
        #If 1 is true and 2 is false shift 1 in rebels favor.
        #Else, Do nothing.
    return modifier

def stack_combat_rating(stack_obj):
    combat_rating = 0

    if (stack_obj.location_id % 10 == 0):           #if true, space combat.
        for militaryunit in stack_obj.militaryunits:
            combat_rating += militaryunit.space_combat
    else:                                           #otherwise, environ combat
        for militaryunit in stack_obj.militaryunits:
            #print "Side: ", militaryunit.side
            #print "Type: ", militaryunit.type
            #print "Mobility: ", militaryunit.mobile
            #print "Environ Combat: ", militaryunit.environ_combat
            #print "Space Combat: ", militaryunit.space_combat
            combat_rating += militaryunit.environ_combat
            #print combat_rating

    return combat_rating

def mil_combat_table(die_roll, combat_odds, is_attacker):
    attacker_wounds = (
            (8, 7, 6, 5, 5, 4, 3, 3, 2, 2, 1),
            (7, 6, 5, 5, 4, 3, 2, 2, 1, 1, 1),
            (7, 5, 5, 4, 3, 2, 2, 2, 1, 1, 1),
            (6, 5, 4, 3, 3, 2, 1, 1, 1, 0, 0),
            (5, 4, 4, 3, 2, 1, 1, 0, 0, 0, 0),
            (4, 4, 3, 3, 1, 0, 0, 0, 0, 0, 0))

    defender_wounds = (
            (0, 0, 0, 0, 0, 0, 1, 2, 2, 3, 4),
            (0, 0, 0, 0, 0, 1, 2, 3, 3, 4, 5),
            (0, 0, 0, 0, 1, 1, 2, 3, 4, 4, 5),
            (0, 0, 1, 1, 1, 2, 3, 3, 4, 5, 6),
            (1, 1, 1, 1, 2, 2, 3, 4, 5, 6, 7),
            (1, 1, 1, 2, 2, 3, 4, 5, 6, 7, 8))
    #print "Die Roll", die_roll+1
    if is_attacker:
        return (attacker_wounds[die_roll][combat_odds])
    else:
        return (defender_wounds[die_roll][combat_odds])
#end Military Combat
