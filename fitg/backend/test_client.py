import rpyc
from service import ClientService
import json
from pprint import pprint

client = rpyc.connect("localhost", 55889, ClientService, config = {"allow_public_attrs" : True})

# Adding validate_only=True to any call will only validate if it's possible.
# You need to catch an IntegrityError when calling this since name is unique
response = client.root.start_game(id="test", player="bob")

print("Starting game test with player bob")
#pprint(response)

glist = client.root.list_games()

print("Listing all games")
pprint(glist)

print("Trying a move")
move = client.root.move(stack_id=1, location_id=1)
pprint(move)


print("Getting state of planets")
planet = client.root.get_state(object_type="Environ")
pprint(planet)

#client.root.combat(attacker_stack_id=1, defender_stack_id=2, options=tuple('2'))
#client.root.split_stack(stack_id=1, unit_id=1, character_id=None)
#client.root.merge_stack(accepting_stack=1, merging_stack=2)
#client.root.draw_mission()
#client.root.show_mission(mission_id=1)
#client.root.show_mission()

# assign mission can be a character id or a tuple of character ids
#client.root.assign_mission(mission_id=1, character_id=1)
#client.root.assign_mission(mission_id=1, character_id=(1, 2, 3, 4))