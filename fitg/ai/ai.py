import rpyc
from fitg.backend import service
import json
from pprint import pprint

client = rpyc.connect("localhost", 55889, service.ClientService)

# COUP : C
# DIPLOMACY : D
# ASSASSINATION: A
# STOP REBELLION: R
# GAIN CHARACTERS: G

# Adding validate_only=True to any call will only validate if it's possible.
# You need to catch an IntegrityError when calling this since name is unique
response = client.root.start_game(name="test", player="bob")

print("Starting game test with player bob")
pprint(response)

glist = client.root.list_games()

print("Listing all games")
pprint(glist)

print("Trying a move")
move = client.root.move(stack_id=1, game_name='test', location_id=1)
pprint(move)

environ_list # = all environs in this scenario

#when it's our turn
while(run):
	reactionMove = False
	if(ourTurn):
		stack_list #g = et our stacks
		character_stack_list # = get our character stack list

		enemy_stack_list # = get their stacks that we can see
		#if any planet is in rebellion
		if planet_in_rebellion:
			client.root.move(character_stack, game_name="test", planet_in_rebellion.location)
			for stack in stack_list:
				client.root.move(stack, game_name="test", planet_in_rebellion.location)
			for enemy_stack in enemy_stack_list:
				if(enemy_stack.location = planet_in_rebellion.location):
					#don't know what my options are
					# probably no options because we want all the characters
					# to be available for missions
					client.root.combat(combined_stack, enemy_stack)
			client.root.assign_mission("R", character_stack)
		else:
			#operations (movement/combat)
			for enemy_stack in enemy_stack_list:
				if(enemy_stack.detected):
					#send the strongest units
					for stack in stack_list:
						#tell them to move even if we can't
						#leaders for the future
						client.root.move(stack, game_name='test', enemy_stack.location)
						#need to combine the stacks for combat
					#combined_stack is the stack at the location we're moving to
					#need to add options (leaders)
					client.root.combat(combined_stack, enemy_stack)
				else:
					for stack in stack_list:
						if random() < 0.20:
							for environ in environ_list:
								if random() < 0.50:
									client.root.move(stack, game_name="test", environ)

			#search (combat)

			#missions
			for character_stack in character_stack_list:
				tmp = random() % 4;
				if tmp == 0:
					# Diplomacy
					client.root.assign_mission("D", character_stack)
				elif tmp == 1:
					# coup
					client.root.assign_mission("C", character_stack)
				elif tmp == 2:
					#assassination
					client.root.assign_mission("A", character_stack)
				else:
					#gain character
					client.root.assign_mission("G", character_stack)
		ourTurn = False
	else:
		#reactionary move?

		enemy_stack_list # get all enemies (even the non-detected ones) sorted list please
		stack_list # get all stacks of military units// sorted list please
		for enemy_stack in enemy_stack_list:
			for stack in stack_list:
				if stack.location != enemy_stack.location and not reactionMove:
					unit = stack.units.pop()
					client.root.move(unit, game_name="test", enemy_stack.location)
					reactionMove = True
				if enemy_stack.location == stack.location:
					#do we search and therefore fight?
					if random() < 0.50:
						Search(stack, enemy_stack)
		#is someone detected in the environ we are in? do we want to search
		#reaction move
		#sleep 10s

#client.root.combat(attacker_stack_id=1, defender_stack_id=2, options=tuple('2'))
#client.root.split_stack(stack_id=1, unit_id=1, character_id=None)
#client.root.merge_stack(accepting_stack=1, merging_stack=2)
#client.root.draw_mission()
#client.root.show_mission(mission_id=1)
#client.root.show_mission()

# assign mission can be a character id or a tuple of character ids
#client.root.assign_mission(mission_id=1, character_id=1)
#client.root.assign_mission(mission_id=1, character_id=(1, 2, 3, 4))