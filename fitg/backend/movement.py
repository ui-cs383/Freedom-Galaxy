from database_creation import loadDatabase
from orm import *
from random import randint


def MoveEnviron(StackID, EnvironID):
	session = Session()

	newloc = session.query(Environ).filter_by(id = EnvironID).one()

	if newloc == None:
		raise Exception("No environ with that ID found")
	oldloc = session.query(Stack).filter_by(id = StackID).one().location
	
	if (int(newloc.id) / 10) != (int(oldloc) / 10):
		raise Exception("Cannot move to non-adjacent environs")

	MovingStack = session.query(Stack).filter_by(id = StackID).one()
	MovingStack.location = newloc.id

	session.add(MovingStack)
	session.commit()

loadDatabase()

MoveEnviron(1,'3110')
MoveEnviron(2,'3112')

session = Session()
print session.query(Stack).filter_by(id = 1).one().location

