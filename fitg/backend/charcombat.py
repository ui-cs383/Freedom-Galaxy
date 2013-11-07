from database_creation import *
from random import randint


def CharCombat(AtkID, DefID):
	session = Session()

	AtkStack = session.query(Stack).filter_by(id = AtkID).one()
	DefStack = session.query(Stack).filter_by(id = DefID).one()

	while AtkStack.inactive != []:
		AtkStack.active.append(AtkStack.inactive.pop())

	CR = 0
	for unit in AtkStack.active:
		CR += session.query(Character).filter_by(name = unit).one().combat

	AtkStack.combatrating = CR
	CD = AtkStack.combatrating - DefStack.combatrating
	print "Computed CombatDifferential: " + str(CD)
	
	# still needs to include breakoff and capture modifiers
	# also decision if firefight or hand-to-hand

	AtkResult = session.query(charCombat).filter_by(dice = randint(1,6)).one().results
	DefResult = session.query(charCombat).filter_by(dice = randint(1,6)).one().results

	AtkWounds = AtkResult[charCombatTranslate(CD)].split('/')[0]
	DefWounds = DefResult[charCombatTranslate(CD)].split('/')[1]

	print "Attacking Stack wounds: " + str(AtkWounds)
	print "Defending Stack wounds: " + str(DefWounds)

	#if '*' in AtkWounds:
	if True:
		print "Captured!"
		AtkStack.captive.append(DefStack.active.pop(randint(0,len(DefStack.active)-1)))
	if '*' in DefWounds:
		print "Captured!"
		AtkStack.captive.append(DefStack.active.pop(randint(0,len(DefStack.active)-1)))

	print "Inside Function:"
	print session.query(Stack).filter_by(id = 2).one().active
	print session.query(Stack).filter_by(id = 1).one().active
	print session.query(Stack).filter_by(id = 2).one().captive	

	session.add(AtkStack, DefStack)
	session.commit()

def charCombatTranslate(CD):
	if CD > 11:
		CD = 11
	elif CD < -7:
		CD = -7

	translator = [0,1,1,1,2,2,3,4,5,6,6,7,7,7,8,8,8,8,9]

	return translator[CD+7] # must shift over for table to align

CharCombat(2,1)

session = Session()
print "Outside Function:"
print session.query(Stack).filter_by(id = 2).one().active
print session.query(Stack).filter_by(id = 1).one().active
print session.query(Stack).filter_by(id = 2).one().captive	