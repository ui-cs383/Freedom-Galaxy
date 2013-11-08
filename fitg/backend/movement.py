from database_creation import *

session = Session()

def MoveEnviron(StackID, EnvironID):
	session = Session()

	newloc = session.query(Environ).filter_by(id = EnvironID).first()

	if newloc == None:
		raise Exception("No environ with that ID found")
	oldloc = session.query(Stack).filter_by(id = StackID).first().location
	
	if (int(newloc.id) / 10) != (int(oldloc) / 10):
		raise Exception("Cannot move to non-adjacent environs")

	MovingStack = session.query(Stack).filter_by(id = StackID).first()
	MovingStack.location = newloc.id

	session.add(MovingStack)
	session.commit()


MoveEnviron(1,'3112')
MoveEnviron(2,'3112')

