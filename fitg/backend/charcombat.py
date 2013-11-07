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

	# still needs to include breakoff and capture modifiers
	# also decision if firefight or hand-to-hand

	AtkResult = session.query(charCombat).filter_by(dice = randint(1,6)).one()
	DefResult = session.query(charCombat).filter_by(dice = randint(1,6)).one()


	print AtkResult.dice

'''	AtkWounds = AtkResult[charCombatTranslate(CD)].split('/')[0]
	DefWounds = DefResult[charCombatTranslate(CD)].split('/')[1]

	if '*' in AtkWounds:
		AtkStack.captives.append(DefStack.active.pop(randint(0,len(DefStack.active)-1)))
	if '*' in DefWounds:
		AtkStack.captives.append(DefStack.active.pop(randint(0,len(DefStack.active)-1)))
'''
	

	#session.add(AtkStack, DefStack)
	#session.commit

def charCombatTranslate(CD):
	if CD > 11:
		CD = 11
	elif CD < -7:
		CD = -7

	translator = ['neg7orless','neg6toneg4','neg6toneg4','neg6toneg4','neg3toneg2',\
					'neg3toneg2','negone','zero','one','twoto3','twoto3','fourto6',\
					'fourto6','fourto6','sevento10','sevento10','sevento10','sevento10','elevenormore']

	return translator[CD+7] # must shift over for table to align

CharCombat(2,1)