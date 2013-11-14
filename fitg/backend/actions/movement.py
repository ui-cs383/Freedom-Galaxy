from database_creation import loadDatabase
from orm import *
from random import randint


def move_environ(stack_id, environ_id):
	session = Session()

	newloc = session.query(Environ).filter_by(id = environ_id).one()

	if newloc == None:
		raise Exception("No environ with that ID found")
	oldloc = session.query(Stack).filter_by(id = stack_id).one().location
	
	if (int(newloc.id) / 10) != (int(oldloc.id) / 10):
		raise Exception("Cannot move to non-adjacent environs")

	moving_stack = session.query(Stack).filter_by(id = stack_id).one()
	moving_stack.location = newloc

	session.add(moving_stack)
	session.commit()

if __name__ == "__main__":
	loadDatabase()

	move_environ(1,'3110')
	move_environ(2,'3112')

	session = Session()
	print session.query(Stack).filter_by(id = 1).one().location

