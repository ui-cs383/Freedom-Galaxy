from database_creation import *
from random import randint


def CharCombat(AtkID, DefID):
	session = Session()

	AtkStack = session.query(Stack).filter_by(id = AtkID).one()
	DefStack = session.query(Stack).filter_by(id = DefID).one()

	# still needs to include breakoff and capture modifiers
	# also decision if firefight or hand-to-hand

	AtkResult = session.query(charCombat).filter_by(dice = randint(1,6)).one().results
	DefResult = session.query(charCombat).filter_by(dice = randint(1,6)).one().results

	session.add(AtkStack, DefStack)
	session.commit()

def charCombatTranslate(CD):
	if CD > 11:
		CD = 11
	elif CD < -7:
		CD = -7

	translator = [0,1,1,1,2,2,3,4,5,6,6,7,7,7,8,8,8,8,9]

	return translator[CD+7] # must shift over for table to align

CharCombat(1,2)
