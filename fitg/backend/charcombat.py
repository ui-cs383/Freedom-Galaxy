from database_creation import loadDatabase
from orm import *
from random import randint

# look at client github
# 

def CharCombat(AtkID, DefID):

	session = Session()

	AtkStack = session.query(Stack).filter_by(id = AtkID).one()
	DefStack = session.query(Stack).filter_by(id = DefID).one()

	# still needs to include breakoff and capture modifiers
	# also decision if firefight or hand-to-hand

	CD = GetStackCombat(AtkID, session) - GetStackCombat(DefID, session)

	AtkResult = CharTable(randint(0,5),CD,True)
	DefResult = CharTable(randint(0,5),CD,False)

	if AtkResult[1] == 1:
		CapturedChar = DefStack.characters[randint(0,len(DefStack.characters)-1)]
		CapturedChar.stack_id = AtkID
		CapturedChar.captive = True
		CapturedChar.active = False

	if DefResult[1] == 1:
		CapturedChar = DefStack.characters[randint(0,len(DefStack.characters)-1)]
		CapturedChar.stack_id = AtkID
		CapturedChar.captive = True
		CapturedChar.active = False

	session.add(AtkStack, DefStack)
	session.commit()

def GetStackCombat(StackID, session):
	CR = 0
	for unit in session.query(Stack).filter_by(id = StackID).first().characters:
		if unit.active == True:
			CR += unit.combat - unit.wounds
	return CR

def CharTable(dice, CD, IsAttacker):
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

loadDatabase()

session = Session()
print session.query(Stack).filter_by(id = 1).one().characters
print "Before:"
for character in session.query(Stack).filter_by(id = 1).one().characters:
	print character
CharCombat(2,1)
print "After:"
for character in session.query(Stack).filter_by(id = 1).one().characters:
	print character
