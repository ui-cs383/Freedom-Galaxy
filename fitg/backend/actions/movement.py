#from database_creation import loadDatabase
from orm import *
from sqlalchemy.orm import exc
from random import randint
from detection_routine import *


def move(session, stack_id, environ_id):
    # need to make sure stack_id and enviorn_id are in the same game
    # this can be checked by ensuring stack.game_id = environ.planet.game_id

    # See if new location can be grabbed
    try:
        newloc = session.query(Environ).filter_by(id = environ_id).one()
    except exc.NoResultFound:
        newloc = None

    # See if old location can be grabbed
    try:
        oldloc = session.query(Stack).filter_by(id = stack_id).one().environ
    except exc.NoResultFound:
        oldloc = None

    # Check if either are None
    if newloc is not None:
        # Check if they aren't adjacent
        if oldloc != None:
            if (oldloc.location != 0) or (newloc.location != 0):
                if (session.query(Stack).filter_by(id = stack_id).one().can_fly()):
                    return False, "Invalid Move, Full Stack does not have space capabilities."
            if oldloc.planet != newloc.planet:
                return False, "Invalid Move, must go through orbit box to travel between planets."
            #    if (oldloc.location != 0) and (newloc.location != 0):
            #        if (session.query(Stack).filter_by(id = stack_id).one().spaceship()):
            #            return False, "Invalid Move, Stack does not have space capabilities."
        else:
            pass
    else:
        # One is None, exit
        return False, "Invalid Move"

    if (newloc.planet.pdb_state != 0) and (session.query(Stack).filter_by(id = stack_id).one().spaceship()):
        detection_routine(session, stack_id, newloc.planet.pdb_level)
    try:
        moving_stack = session.query(Stack).filter_by(id = stack_id).one()
    except:
        success = False
    else:
        success = True
        moving_stack.environ = newloc
        session.add(moving_stack)

    if success:
        session.commit()
        return success, moving_stack.__dict__
    else:
        return success, "FATAL: Unable to find stack!"

def merge_stack(session, src_id, des_id):

    src_stack = session.query(Stack).filter_by(id = src_id).one()
    des_stack = session.query(Stack).filter_by(id = des_id).one()

    # check if stacks are same team? same location?

    try:
        assert src_stack.environ_id == des_stack.environ_id
        assert src_stack.side() == des_stack.side()
    except:
        success = False
    else:
        success = True
        for character in src_stack.characters:
            character.stack_id = des_id
        for unit in src_stack.units:
            unit.stack_id = des_id

    if success:
        session.add(des_stack)
        session.delete(src_stack)
        session.commit()
        return success, { 'stack': des_stack.__dict__ }
    else:
        return success, "FATAL: Stacks cannot be merged"

def split_stack(session, stack_id, unit_id=None, character_id=None):
    stack = session.query(Stack).filter_by(id = stack_id).one()

    try:
        if character_id:
            unit = session.query(Character).filter_by(id = character_id).one()
        else:
            unit = session.query(Unit).filter_by(id = unit_id).one()
    except:
        success = False
    else:
        success = True
        unit_stack = Stack(stack.environ_id, stack.game_id)
        session.add(unit_stack, unit)

        if character_id:
            unit_stack.characters.append(unit)
        else:
            unit_stack.units.append(unit)

    if not stack.characters and not stack.units:
        session.delete(stack)
        
    if success:
        session.commit()
        if character_id:
            unit = session.query(Character).filter_by(id = character_id).one()
        else:
            unit = session.query(Unit).filter_by(id = unit_id).one() 
        stack = session.query(Stack).filter_by(id = unit.id).one()
        return success, { 'stack': unit_stack.__dict__ , 'unit': unit.__dict__}
    else:
        return success, "FATAL: Unable to split stack"
