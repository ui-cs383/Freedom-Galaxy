import rpyc
import service

client = rpyc.connect("localhost", 55889, service.ClientService)

# Adding validate_only=True to any call will only validate if it's possible.
response = client.root.start_game(name="test", player="bob")

print("Starting game test with player bob")
print(response)

response2 = client.root.start_game(name="test2", player="jeff", scenario="demo")

print("Starting game test2 with player jeff and scenario demo")
print(response2)

#client.root.move(stack_id=1, location_id=1101)
#client.root.combat(attacker_stack_id=1, defender_stack_id=2, options=tuple('2'))
#client.root.split_stack(stack_id=1, unit_id=1, character_id=None)
#client.root.merge_stack(accepting_stack=1, merging_stack=2)
#client.root.draw_mission()
#client.root.show_mission(mission_id=1)
#client.root.show_mission()

# assign mission can be a character id or a tuple of character ids
#client.root.assign_mission(mission_id=1, character_id=1)
#client.root.assign_mission(mission_id=1, character_id=(1, 2, 3, 4))