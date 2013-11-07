from database_creation import *


def MoveStack(StackID, Location):
	session = Session()

	newloc = session.query(Environ).filter_by(id = Location).first()
	oldloc = session.query(Stack).filter_by(id = StackID).first().location
	# test if possible move

	MovingStack = session.query(Stack).filter_by(id = StackID).first()
	MovingStack.location = newloc.id

	session.add(MovingStack)
	session.commit()



MoveStack(1,'1121')
MoveStack(2,'1131')

session = Session()

print session.query(Stack).filter_by(id = 1).one().location