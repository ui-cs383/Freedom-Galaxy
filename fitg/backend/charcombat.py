from database_creation import *
from random import randint

session = Session()

def CharCombat(AtkID, DefID):

	AtkStack = session.query(Stack).filter_by(id = AtkID).one()
	DefStack = session.query(Stack).filter_by(id = DefID).one()

	# still needs to include breakoff and capture modifiers
	# also decision if firefight or hand-to-hand

	CD = GetStackCombat(AtkID) - GetStackCombat(DefID)

	AtkResult = session.query(charCombat).filter_by(dice = randint(1,6)).one().results
	DefResult = session.query(charCombat).filter_by(dice = randint(1,6)).one().results

	AtkWounds = AtkResult[charCombatTranslate(CD)].split('/')[0]
	DefWounds = DefResult[charCombatTranslate(CD)].split('/')[1]

	if '*' in AtkWounds:
		CapturedChar = DefStack.characters[randint(0,len(DefStack.characters)-1)]
		CapturedChar.stack_id = AtkID
		CapturedChar.captive = True
		CapturedChar.active = False

	if '*' in DefWounds:
		CapturedChar = DefStack.characters[randint(0,len(DefStack.characters)-1)]
		CapturedChar.stack_id = AtkID
		CapturedChar.captive = True
		CapturedChar.active = False

	session.add(AtkStack, DefStack)
	session.commit()

def GetStackCombat(StackID):
	CR = 0
	for unit in session.query(Stack).filter_by(id = StackID).first().characters:
		if unit.active == True:
			CR += unit.combat - unit.wounds
	return CR

def charCombatTranslate(CD):
	if CD > 11:
		CD = 11
	elif CD < -7:
		CD = -7

	translator = [0,1,1,1,2,2,3,4,5,6,6,7,7,7,8,8,8,8,9]

	return translator[CD+7] # must shift over for table to align

CharCombat(1,2)

for unit in session.query(Stack).filter_by(id = 1).first().characters:
	print unit
	if unit.captive == True:
		print "CAPTIVE"
