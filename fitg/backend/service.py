import rpyc

class FreedomService(rpyc.Service):
    ALIASES = ["fitg"]

    def on_connect(self):

        pass

    def on_disconnect(self):
        pass

    def exposed_move(self, stack_id, location_id, validate_only=False):
        assert isinstance(stack_id, int)
        assert isinstance(location_id, int)
        logger.info("Action: Move stack " + str(stack_id) + " to location " + str(location_id))

    def exposed_combat(self, attacker_stack, defender_stack, options, validate_only=False):
        assert isinstance(attacker_stack, int)
        assert isinstance(defender_stack, int)

        logger.info("Action: Calculate combat outcome for attacker " + str(attacker_stack) + " and " + str(defender_stack))

    def exposed_split_stack(self, stack_id, unit_id=None, character_id=None, validate_only=False):
        assert isinstance(stack_id, int)
        assert isinstance(character_id, int) or isinstance(unit_id, int)

        unit = unit_id or character_id
        logger.info("Action: Split unit " + str(unit) + " from stack " + str(stack_id))

    def exposed_merge_stack(self, accepting_stack, merging_stack):
        assert isinstance(accepting_stack, int)
        assert isinstance(merging_stack, int)

        logger.info("Action: Merge stack " + str(merging_stack) + " into " + str(accepting_stack))

    def exposed_show_mission(self, mission_id=None):
        if mission_id is None: 
            logger.info("Action: Displaying mission information for all missions")
        else:
            logger.info("Action: Displaying mission information for mission " + str(mission_id))

    def exposed_draw_mission(self):
        logger.info("Action: Drawing a mission card")

    def exposed_assign_mission(self, mission_id, character_id):
        assert isinstance(mission_id, int)

        try:
            assert isinstance(character_id, int)
            logger.info("Action: Assign mission " + str(mission_id) + " to character " + str(character_id))
        except AssertionError:
            assert isinstance(character_id, tuple)
            logger.info("Action: Assign mission " + str(mission_id) + " to character " + str(character_id))


if __name__ == "__main__":
    import logging
    from rpyc.utils.server import ThreadedServer

    host = 'localhost'
    port = 18861

    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    t = ThreadedServer(FreedomService, port = 18861)
    logger.info('Starting server on ' + host + ':' + str(port))
    t.start()