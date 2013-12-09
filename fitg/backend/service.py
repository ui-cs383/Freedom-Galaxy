import rpyc
from contextlib import contextmanager

@contextmanager
def session_scope(orm):
    """Provide a transactional scope around a series of operations."""
    session = orm.Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class ClientService(rpyc.Service):
    """Handles service calls to the client.

    A single-method class for handling callbacks from the server which aren't a response 
    to a client-initiated request (such as the other player moving).
    """
    ALIASES = ["client"]

    def exposed_state_change(self, response):
        """Returns the current turn state.

        Any time a state change is intitiated by a client other than the current client, state_change is called 
        on any other client that is attached to the game in question. This method must be implemented by the 
        client application, and will raise a NotImplementedError if called without overriding.

        :param response: The response that was sent to the client that initiated the request.
        :type response: dict.
        :returns:  dict -- the current game state.
        :raises: NotImplementedError
        """
        raise NotImplementedError


class FreedomService(rpyc.Service):
    ALIASES = ["fitg"]

    def __init__(self, conn):
        super(FreedomService, self).__init__(conn)
        import orm
        import actions

        self.actions = actions
        self.orm = orm
        self.logger = self._conn._config['logger']

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def response(self, called, parameters, success, result):
        if result is not None:
            if 'self' in result: del result['self']

        response = { 'request': dict(), 'response': dict() }

        response['request']['call'] = called
        response['request']['parameters'] = parameters
        response['request']['success'] = success
        response['response'] = result

        return response

    def exposed_turn_state(self, validate_only=False):
        """Returns the current turn state.

        :param validate_only: If true the move will only be validated.
        :type validate_only: bool.
        :returns:  dict -- the current game state.
        :raises: AssertionError
        """
        self.logger.info("requested current turn state")

    def exposed_start_game(self, name, player, scenario="demo", ai=False, validate_only=False):
        """Start a new game.

        Creates a new game.
        How do we initialize this call to another player? The AI?
        Will this assert anything?

        :param validate_only: If true the move will only be validated.
        :type validate_only: bool.
        :returns:  bool -- True on game creation, false on error.
        :raises: AssertionError
        """
        assert isinstance(name, str)
        assert isinstance(ai, bool)
        assert isinstance(validate_only, bool)

        with session_scope(self.orm) as session:
            self.logger.info("creating a new game")

            request = locals()
            result = self.actions.game.start(session, name, player, scenario)

            return self.response('start_game', request, result[0], result[1])

    def exposed_list_games(self):
        with session_scope(self.orm) as session:

            self.logger.info("getting a list of available games")

            request = locals()
            result = self.actions.game.list(session)

            return self.response('list_games', request, result[0], result[1])

    def exposed_move(self, stack_id, location_id, validate_only=False):
        """Move a stack to a location.

        Move takes a stack_id and moves it to location_id. If stack_id is in an enviorn and location_id 
        is an adjacent enviorn, a environ based move is completed. If location_id is a different enviorn a space
        move is completed.

        :param stack_id: The stack_id of the stack to be moved.
        :type stack_id: int.
        :param location_id: Current state to be in.
        :type location_id: int.
        :param validate_only: If true the move will only be validated.
        :type validate_only: bool.
        :returns:  dict -- a dictionary of updated stack locations.
        :raises: AssertionError
        """

        assert isinstance(game_name, str)
        assert isinstance(stack_id, int)
        assert isinstance(location_id, int)

        with session_scope(self.orm) as session:
            self.logger.info("requested stack " + str(stack_id) + " movement to location " + str(location_id))

            request = locals()
            result = self.actions.movement.move(session, game_name, stack_id, location_id)

            return self.response('move', request, result[0], result[1])

    def exposed_combat(self, attacker_stack_id, defender_stack_id, options, validate_only=False):
        """Start combat between an attacker and a defender.

        Move takes a stack_id and moves it to location_id. If stack_id is in an enviorn and location_id 
        is an adjacent enviorn, a environ based move is completed. If location_id is a different enviorn a space
        move is completed.

        :param attacker_stack_id: The unique id of the attacking stack.
        :type attacker_stack_id: int.
        :param defender_stack_id: The unique id of the defending stack.
        :type defender_stack_id: int.
        :param options: A tuple of flags as options for combat.
        :type options: tuple.
        :param validate_only: If true the move will only be validated.
        :type validate_only: false.
        :returns:  dict -- the results of the combat
        :raises: AssertionError
        """
        assert isinstance(attacker_stack_id, int)
        assert isinstance(defender_stack_id, int)

        self.logger.info("requested combat outcome for attacker " + str(attacker_stack_id) + " and " + str(defender_stack_id))

    def exposed_split_stack(self, stack_id, unit_id=None, character_id=None, validate_only=False):
        """Move a stack to a location.

        Move takes a stack_id and moves it to location_id. If stack_id is in an enviorn and location_id 
        is an adjacent enviorn, a environ based move is completed. If location_id is a different enviorn a space
        move is completed.

        :param stack_id: The stack_id of the stack to be moved.
        :type name: int.
        :param unit_id: A tuple of unit_id's to assign to a new stack.
        :type unit_id: tuple or None.
        :param character_id: A tuple of character_id's to assign to a new stack.
        :type character_id: tuple or None.
        :param validate_only: If true the move will only be validated.
        :type validate_only: false.
        :returns:  dict -- a dictionary of stacks with a stack_id parameter.
        :raises: AssertionError
        """
        assert isinstance(stack_id, int)
        assert isinstance(character_id, int) or isinstance(unit_id, int)

        self.logger.info("requested split unit " + str(unit_id) or str(character_id) + " from stack " + str(stack_id))

    def exposed_merge_stack(self, source_stack, destination_stack, validate_only=False):
        """Merges merging_stack into accepting_stack.

        Move takes a stack_id and moves it to location_id. If stack_id is in an enviorn and location_id 
        is an adjacent enviorn, a environ based move is completed. If location_id is a different enviorn a space
        move is completed.

        :param stack_id: The stack_id of the stack to be moved.
        :type name: int.
        :param unit_id: A tuple of unit_id's to assign to a new stack.
        :type unit_id: tuple or None.
        :param character_id: A tuple of character_id's to assign to a new stack.
        :type character_id: tuple or None.
        :param validate_only: If true the move will only be validated.
        :type validate_only: false.
        :returns:  dict -- a dictionary of stacks with a stack_id parameter.
        :raises: AssertionError
        """
        assert isinstance(accepting_stack, int)
        assert isinstance(merging_stack, int)

        self.logger.info("requested stack merge of " + str(merging_stack) + " into " + str(accepting_stack))

        try:
            actions.movement.merge_stack(session, source_stack, destination_stack):
        except AssertionError:
            self.logger.warn("merge of " + str(merging_stack) + " into " + str(accepting_stack) + " failed")


    def exposed_show_mission(self, mission_id=None, validate_only=False):
        """Shows all missions or details of an existing mission.

        Move takes a stack_id and moves it to location_id. If stack_id is in an enviorn and location_id 
        is an adjacent enviorn, a environ based move is completed. If location_id is a different enviorn a space
        move is completed.

        :param stack_id: The stack_id of the stack to be moved.
        :type name: int.
        :param unit_id: A tuple of unit_id's to assign to a new stack.
        :type unit_id: tuple or None.
        :param character_id: A tuple of character_id's to assign to a new stack.
        :type character_id: tuple or None.
        :param validate_only: If true the move will only be validated.
        :type validate_only: false.
        :returns:  dict -- a dictionary of stacks with a stack_id parameter.
        :raises: AssertionError
        """
        assert isinstance(mission_id, int) or mission_id is None

        if mission_id is None: 
            self.logger.info("requested mission information for all missions")
        else:
            self.logger.info("requested mission information for mission " + str(mission_id))

    def exposed_draw_mission(self, validate_only=False):
        """Draws mission card.

        :param validate_only: If true the move will only be validated.
        :type validate_only: false.
        :returns:  dict -- the current game state.
        """
        self.logger.info("requested a mission")

    def exposed_assign_mission(self, mission_id, character_id, validate_only=False):
        """Draws mission card.

        :param validate_only: If true the move will only be validated.
        :type validate_only: false.
        :returns: dict -- the curent game state.
        """
        assert isinstance(mission_id, int)

        try:
            assert isinstance(character_id, int)
            self.logger.info("requested mission " + str(mission_id) + " assignment to character " + str(character_id))
        except AssertionError:
            assert isinstance(character_id, tuple)
            self.logger.info("requested mission " + str(mission_id) + " assignment to characters " + str(character_id))


if __name__ == "__main__":
    import logging
    from rpyc.utils.server import ThreadedServer

    host = 'localhost'
    port = 18861

    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    t = ThreadedServer(FreedomService, port = 18861)
    t.start()