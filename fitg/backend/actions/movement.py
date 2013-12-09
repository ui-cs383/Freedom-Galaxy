#from database_creation import loadDatabase
from orm import *
from sqlalchemy.orm import exc
from random import randint


def move(session, stack_id, environ_id):
    # need to make sure stack_id and enviorn_id are in the same game
    # this can be checked by ensuring stack.game_id = environ.planet.game_id

    try:
        newloc = session.query(Environ).filter_by(id = environ_id).one()
    except exc.NoResultFound:
        success = False
    else:
        success = True

    try:
        oldloc = session.query(Stack).filter_by(id = stack_id).one().location
    except exc.NoResultFound:
        success = False
    else:
        success = True

    if success:
        if (int(newloc.id) / 10) != (int(oldloc.id) / 10):
            success = False

    # if moving to Orbit (environ id ends in '0') then PDB routines ?
    try:
        moving_stack = session.query(Stack).filter_by(id = stack_id).one()
    except exc.NoResultFound:
        success = False
    else:
        success = True
        moving_stack.location = newloc
        session.add(moving_stack)

    if success:
        session.commit()
        return success, moving_stack.__dict__
    else:
        return success, None

def merge_stack(session, src_id, des_id):

    src_stack = session.query(Stack).filter_by(id = src_id).one()
    des_stack = session.query(Stack).filter_by(id = des_id).one()

    #assert isinstance(src_stack, Stack)
    #assert isinstance(des_stack, Stack)

    # check if stacks are same team? same location?

    assert src_stack.location == des_stack.location

    for character in src_stack.characters:
        character.stack_id = des_id
    for unit in src_stack.militaryunits:
        unit.stack_id = des_id

    session.add(des_stack)
    session.delete(src_stack)
    session.commit()

if __name__ == "__main__":
    loadDatabase()

    #move_environ(1,'3110')
    #move_environ(2,'3112')

    session = Session()
    print session.query(Stack).filter_by(id = 1).one().location
    
    merge_stack(1,2)
    print session.query(Stack).filter_by(id = 2).one().characters