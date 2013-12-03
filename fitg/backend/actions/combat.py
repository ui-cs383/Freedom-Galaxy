#from database_creation import loadDatabase
from orm import *
from random import randint

session = Session()
 
def char_combat(atk_id, def_id, options):

    session = Session()

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

    session.commit()

def char_wounds(stack, num_wounds, session):
    while num_wounds > 0 and stack.characters:
        victim = stack.characters[randint(0,len(stack.characters)-1)]
        session.add(victim)
        victim.wounds += 1
        print victim.name, " suffers wound!"
        if victim.wounds >= victim.endurance:
            print victim.name, " has died! :("
            session.delete(victim)
        num_wounds -= 1

    session.commit()

def char_combat_rating(stack, session):
    CR = 0
    for character in stack.characters:
        if character.active == True:
            CR += character.combat - character.wounds
    return CR

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

#Authored By Ben Cumber
#military_units.dat info format
#side, type, mobility, environ combat, space combat
def mil_combat(atk_id, def_id):
    session = Session()

    atk_stack = session.query(Stack).filterby(id = atk_id).one()
    def_stack = session.query(Stack).filterby(id = def_id).one()

    atk_mil_units = atk_stack.militaryunits
    def_mil_units = def_stack.militaryunits


def mil_combat_table(die_roll, combat_odds, is_attacker):
    defender_wounds = (
            (8, 7, 6, 5, 5, 4, 3, 3, 2, 2, 1),
            (7, 6, 5, 5, 4, 3, 2, 2, 1, 1, 1),
            (7, 5, 5, 4, 3, 2, 2, 2, 1, 1, 1),
            (6, 5, 4, 3, 3, 2, 1, 1, 1, 0, 0),
            (5, 4, 4, 3, 2, 1, 1, 0, 0, 0, 0),
            (4, 4, 3, 3, 1, 0, 0, 0, 0, 0, 0))
    
    attacker_wounds = (
            (0, 0, 0, 0, 0, 0, 1, 2, 2, 3, 4),
            (0, 0, 0, 0, 0, 1, 2, 3, 3, 4, 5),
            (0, 0, 0, 0, 1, 1, 2, 3, 4, 4, 5),
            (0, 0, 1, 1, 1, 2, 3, 3, 4, 5, 6),
            (1, 1, 1, 1, 2, 2, 3, 4, 5, 6, 7),
            (1, 1, 1, 2, 2, 3, 4, 5, 6, 7, 8))


if __name__ == "__main__":
    loadDatabase()

    session = Session()

    char_combat(1,2,'C')


    session.commit()

