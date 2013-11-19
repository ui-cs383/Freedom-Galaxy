from database_creation import loadDatabase
from orm import *
from random import randint


def char_combat(AtkID, DefID, Options):

	session = Session()

	atk_stack = session.query(Stack).filter_by(id = AtkID).one()
	def_stack = session.query(Stack).filter_by(id = DefID).one()

	# still needs to include breakoff and capture modifiers
	# also decision if firefight or hand-to-hand

	CD = char_combat_rating(AtkID, session) - char_combat_rating(DefID, session)

	if 'C' in Options:
		CD -= 2

	atk_result = char_table(randint(0,5),CD,True)
	def_result = char_table(randint(0,5),CD,False)

	if 'F' in Options:
		atk_result[0] *= 2
	if atk_stack.militaryunits:
		atk_result[0] *= 2
		
	if 'C' in Options:
		if atk_result[1] == 1:
			CapturedChar = def_stack.characters[randint(0,len(def_stack.characters)-1)]
			CapturedChar.stack_id = AtkID
			CapturedChar.captive = True
			CapturedChar.active = False

		if def_result[1] == 1:
			CapturedChar = def_stack.characters[randint(0,len(def_stack.characters)-1)]
			CapturedChar.stack_id = AtkID
			CapturedChar.captive = True
			CapturedChar.active = False

	session.add(atk_stack, def_stack)
	session.commit()

def suffer_wounds(character, num, session):
	pass

def char_combat_rating(StackID, session):
	CR = 0
	for character in session.query(Stack).filter_by(id = StackID).one().characters:
		if character.active == True:
			CR += character.combat - character.wounds
	return CR

def char_table(dice, CD, IsAttacker):
	AttackerWounds = (
		(4,3,3,2,2,2,2,1,1,1),(4,3,2,2,2,1,1,1,1,0),(3,3,2,2,1,1,1,1,0,0),
		(3,2,2,1,1,1,0,0,0,0),(2,2,1,1,0,0,0,0,0,0),(2,1,0,0,0,0,0,0,0,0))

	DefenderWounds = (
		(0,0,0,0,0,0,0,1,1,2),(0,0,0,0,0,0,1,1,1,2),(0,0,0,0,0,1,1,1,2,3),
		(0,0,0,1,1,1,1,2,3,3),(0,0,1,1,1,1,2,2,3,4),(1,1,1,1,2,2,2,3,3,4))

	AttackerCapture = (
		(0,0,0,0,0,1,0,0,0,0),(0,0,0,1,1,0,1,1,1,0),(0,1,0,0,0,0,0,0,0,0),
		(0,0,1,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,1,0,0),(0,0,0,0,0,0,0,0,0,0))

	DefenderCapture = (
		(0,0,0,0,0,0,0,0,1,0),(0,0,0,0,0,0,0,0,0,0),(0,0,0,0,1,0,0,1,1,0),
		(0,0,0,1,0,1,1,1,0,0),(0,0,0,0,0,0,1,0,1,0),(0,0,0,0,0,0,0,0,0,0))

	if IsAttacker:
		return (AttackerWounds[dice][CD], AttackerCapture[dice][CD])
	else:
		return (DefenderWounds[dice][CD], DefenderCapture[dice][CD])

#Authored By Ben Cumber
#military_units.dat info format
#side, type, mobility, environ combat, space combat
def mil_combat(atk_id, def_id):
    session = Session()

    atk_stack = session.query(Stack).filter_by(id = atk_id).one()
    def_stack = session.query(Stack).filter_by(id = def_id).one()

    #atk_mil_units = atk_stack.militaryunits
    #def_mil_units = def_stack.militaryunits
    atk_combat_rating = stack_combat_rating(atk_stack)
    def_combat_rating = stack_combat_rating(def_stack)
    
    column = stack_combat_ratio(atk_combat_rating, def_combat_rating)
    print "Attacker Combat Rating: ", atk_combat_rating
    print "Defender Combat Rating: ", def_combat_rating

    
    #atk_result = mil_combat_table(randint(0, 5), combat_ratio, True)
    #def_result = mil_combat_table(randint(0, 5), combat_ratio, False)

def stack_combat_ratio(atk_rating, def_rating):     #Always round in the
    ratio = 0                                       #defenders favor
    if(atk_rating > def_rating):
        ratio =  atk_rating / def_rating
    elif(atk_rating < def_rating):
        ratio = def_rating / atk_rating
        ratio += 1
    else:
        #they are equal, the ratio is 1:1, column 5
        ratio = 5
    print "Ratio = ", ratio
    return ratio


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
    if is_attacker:
        return (attacker_wounds[die_roll][combat_odds])
    else:
        return (defender_wounds[die_roll][combat_odds])


if __name__ == "__main__":
    loadDatabase()

    session = Session()
    #Character Combat Tests
    #print session.query(Stack).filter_by(id = 1).one().characters
    #print "Before:"
    #for character in session.query(Stack).filter_by(id = 1).one().characters:
    #        print character
    #char_combat(2,1,'C')
    #print "After:"
    #for character in session.query(Stack).filter_by(id = 1).one().characters:
    #        print character


    #Military Combat Tests
    print session.query(Stack).filter_by(id = 3).one().militaryunits
    print session.query(Stack).filter_by(id = 4).one().militaryunits
    print "Combat Ratings should be 4 and 2"
    mil_combat(3, 4)
    stack_combat_ratio(15, 5)
    session.commit()

