import rpyc
from fitg.backend import service
import json
from pprint import pprint
import time

class AI:
	'''
	This class will construct an AI object that will connect to 
	the server and act as a client in the game.

	'''

	def __init__(self, connection_options=None):
		# Eventually get the config options and use them to
		# connect to the server.

		# self.response will be the object that stores the backend response
		# received from a given call to the backend
		self.client = rpyc.connect("localhost", 55889, service.ClientService)
		self.response = None
		self.connection_options = connection_options

	def start_game(self):
		# Eventually get the config options and use them to define the game

		game_list = self.client.root.list_games()
		print("Listing all games")
		pprint(glist)

		environ_list = self.client.root.get_state(gameid, "environ")# = all environs in this scenario

		# Adding validate_only=True to any call will only validate if 
		# it's possible.
		# You need to catch an IntegrityError when calling this since 
		# name is unique
		self.response = self.client.root.start_game(name="test", 
											   player="bob")
		print("Starting game test with player bob")
		pprint(response)

	def run(self):	
		# COUP : C
		# DIPLOMACY : D
		# ASSASSINATION: A
		# STOP REBELLION: R
		# GAIN CHARACTERS: G
		environ_list = self.client.root.get_state(gameid, "Environ")# = all environs in this scenario
		# when it's our turn
		while(True):
			reactionMove = False
			if(ourTurn):
				#reset the lists because they can/will change
				our_unit_stack_list = []
				their_unit_stack_list = []
				our_characters = []
				their_characters = []
				global_stack_list = self.client.root.get_state(gameid, "Stack") #get our stacks
				character_stack_list = self.client.root.get_state(gameid, "Character")
				for stack in global_stack_list.units:
					if stack.side == "Imperial":
						our_unit_stack_list.append(stack)
					else:
						their_unit_stack_list.append(stack)
				for stack in character_stack_list:
					if stack.side == "Imperial":
						our_characters.append(stack)
					else:
						their_characters.append(stack)

				# enemy_character_stack_list
				#if any planet is in rebellion
				# is this an ID or an object?
				planet = planet_in_rebellion()
				if planet is not None:
					tmpEnviron
					# this is NOT for combat 
					self.client.root.move(our_characters, planet.location)
					
					#need to grab an environ for the planet
					#grab the last environ just to get something
					for environ in planet.environs:
						tmpEnviron = environ
					MoveStrongestUnits(tmpEnviron.id)
					for enemy_stack in enemy_stack_list:
						if(enemy_stack.stack_detection() && enemy_stack.environ_id == tmpEnviron.id):
							# don't know what my options are
							# probably no options because we want 
							# all the characters to be available for missions
							self.client.root.combat(combined_stack, enemy_stack)
					self.client.root.assign_mission("R", character_stack)
				else:
					#operations (movement/combat)
					for enemy_stack in enemy_stack_list:
						#check to see if any of them are detected
						if(enemy_stack.stack_detection()):
							#send the strongest units
							MoveStrongestUnits(enemy_stack.environ_id)
							for stack in stack_list:
								#tell them to move even if we can't
								#leaders for the future
								self.client.root.move(stack,
													  game_name='test', 
													  enemy_stack.location)
							# need to combine the stacks for combat
							# combined_stack is the stack at the location 
							# we're moving to.
							# need to add options (leaders)
							self.client.root.combat(combined_stack,
													enemy_stack)
						else:
							for stack in stack_list:
								if random() < 0.20:
									for environ in environ_list:
										if random() < 0.50:
											self.client.root.move(
														stack,
														game_name="test",
														environ)

					#search (combat)
					# TBD

					#missions
					for character_stack in character_stack_list:
						tmp = random() % 4;
						if tmp == 0:
							# Diplomacy
							self.client.root.assign_mission("D",
															character_stack)
						elif tmp == 1:
							# coup
							self.client.root.assign_mission("C",
															character_stack)
						elif tmp == 2:
							#assassination
							self.client.root.assign_mission("A",
															character_stack)
						else:
							#gain character
							self.client.root.assign_mission("G",
															character_stack)
				ourTurn = False
			else:
				#reactionary move?
				# do we want this at all?
				for enemy_stack in their_unit_stack_list:
					for stack in our_unit_stack_list:
						if stack.environ_id != enemy_stack.environ_id 
											 and not reactionMove:
							unit = self.client.root.split_stack(stack.id)

							self.client.root.move(unit.stack_id,
												  game_name="test",
												  enemy_stack.location)
							reactionMove = True
						if enemy_stack.location == stack.location:
							#do we search and therefore fight?
							if random() < 0.50:
								#search not yet implemented
								#Search(stack, enemy_stack)
				#is someone detected in the environ we are in? do we want 
				# to search?
				#reaction move
			
			# Don't want to poll the system, so sleep for 10 seconds
			# because the backend won't put us to sleep.
			time.sleep(10)

def MoveStrongestUnits(environid):
	environ = self.client.root.get_state(gameid, "environ", environid)
	stack_list # = get all stacks
	num_units = 0 #want to make sure that we don't send too many units over
	new_location_stack #need a new location stack to append to
	#
	while(num_units < environ.size):
		best_attack = 0 # want to start with 0
		best_unit # the unit that has the best attack after each iteration
		best_stack # the stack that contains the best unit
		for stack in stack_list:
			for unit in stack:
				if best_attack < unit.environ_combat && unit.mobile:
					best_attack = unit.environ_combat
					best_unit = unit
					best_stack = stack
		if best_attack != 0:
			moving_stack = self.client.root.split_stack(session, best_stack.id, best_unit.id, False)
			self.client.root.move(session, moving_stack, environ.id)
			if(num_units == 0):
				new_location_stack = moving_stack
			else:
				self.client.root.merge_stack(session, moving_stack, new_location_stack)

		num_units += 1

def planet_in_rebellion():
	list_of_planets = self.client.root.get_state(gameid, "Planet")
	for planet in list_of_planets:
		if planet.in_rebellion:
			return planet
	return None


if __name__ == '__main__':
	ai = AI()
	exit_value = AI.run()