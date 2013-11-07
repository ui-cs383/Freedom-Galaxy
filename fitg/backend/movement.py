from database_creation import *


def MoveStack(StackID, Location):
	session = Session()

	newloc = session.query(Environ).filter_by(id = Location).first()
	oldloc = session.query(Stack).filter_by(id = StackID).first().location
	# test if possible move

	MovingStack = session.query(Stack).filter_by(id = StackID).first()
	print "Moving Stack: " + str(StackID) + " from " + str(oldloc) + " to " + str(newloc.id)
	print "This stack contains: " + str(session.query(Stack).filter_by(id = StackID).first().characters)
	MovingStack.location = newloc.id

	session.add(MovingStack)
	session.commit()



MoveStack(1,'1121')
#MoveStack(2,'1131')

session = Session()

print session.query(Stack).filter_by(id = 1).one().location