from database_creation import *
from mappings import *

def MoveStack(StackID, Location):
	session = Session()

	newloc = session.query(Environs).filter_by(id = Location).one()
	oldloc = session.query(Stacks).filter_by(id = StackID).one().location

	# test if possible move

	MovingStack = session.query(Stack).filter(Stack.id==StackID).one()
	MovingStack.location = newloc.id


	session.add(MovingStack)
	session.commit()



MoveStack(1,'1121')
MoveStack(2,'1131')