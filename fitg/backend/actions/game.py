import yaml
import orm
from sqlalchemy import or_

def start(session, name, player, scenario="egrix"):
	f = 'scenarios/' + scenario + '.yaml'

	with open (f, "r") as scenario_file:
		game_data = scenario_file.read()

	game_data = yaml.load(game_data)

	game = orm.Game(name = name, player1 = player, player2 = None, scenario = scenario)
	stack = orm.Stack()

	for objects, values in game_data.items():
		if objects == 'characters':
			for attributes in values:
				character = orm.Character(**attributes)
				stack.characters.append(character)

	game.stacks.append(stack)


	try: 
		session.add(game)
	except:
		success = False
	else:
		success = True

	return success, { 'game': game.__dict__ }
	

def join(session, name, player):
	game = session.query(orm.Game).filter_by(name = name).filter(or_(player1 = None, player2 = None)).one()
	session.add(game)

	if game.player1 is None:
		game.player1 = player
	elif game.player2 is None:
		game.player2 = player
	else:
		return False, { 'game': game.__dict__ }

	session.add(game)
	session.commit()

	return True, { 'game': game.__dict__ }


def list(session):
	games = session.query(orm.Game).filter((orm.Game.player1 == None) | (orm.Game.player2 == None)).all()
	glist = [ x.__dict__ for x in games ]

	return True, { 'games': glist }


def get_object(session, table, name=None):

	orm_name = getattr(orm, table)

	if name is None:
		items = session.query(orm_name).filter_by(name=name).one()
	else:
		items = session.query(orm_name).all()
		items = [ x.__dict__ for x in items ]

	return True, { table: items }