#from database_creation import loadDatabase
from orm import *
from sqlalchemy.orm import exc
from random import randint


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
    if newloc is not None and oldloc is not None:
        # Check if they aren't adjacent
        if oldloc.planet == newloc.planet and (newloc.location - 1 == oldloc or newloc.location + 1 == oldloc.location):
            return False, "Invalid Move"
    else:
        # One is None, exit
        return False, "Invalid Move"

    # if moving to Orbit (environ id ends in '0') then PDB routines ?
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
        assert src_stack.location == des_stack.location
        assert src_stack.characters[0].side == des_stack.characters[0].side
    except:
        success = False
    else:
        success = True
        for character in src_stack.characters:
            character.stack_id = des_id
        for unit in src_stack.militaryunits:
            unit.stack_id = des_id

    if success:
        session.add(des_stack)
        session.delete(src_stack)
        session.commit()
        return success, { 'stack': des_stack.__dict__ }
    else:
        return success, "FATAL: Stacks cannot be merged"

def split_stack(session, stack_id, unit_id, is_character):
    stack = session.query(Stack).filter_by(id = stack_id).one()

    try:
        if is_character:
            unit = session.query(Character).filter_by(id = unit_id).one()
        else:
            unit = session.query(Unit).filter_by(id = unit_id).one()
    except:
        success = False
    else:
        success = True
        unit_stack = Stack()

        if is_character:
            unit_stack.characters.append(unit)
        else:
            unit_stack.units.append(unit)
        
    if success:
        session.commit()
        return success, { 'stack': new_stack.__dict__ }
    else:
        return success, "FATAL: Unable to split stack"
