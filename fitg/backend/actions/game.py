import yaml
import orm
from sqlalchemy import or_

session = orm.Session()

def start(name, player, scenario="demo"):
	game = orm.Game(name = name, player1 = player, player2 = None, scenario = scenario)

	response = dict()

	try: 
		session.add(game)
	except:
		success = False
	else:
		success = True

	return success, { 'game': game.__dict__ }
	

def join(name, player):
	game = session.query(Game).filter_by(name = name).filter(_or(player1 = None, player2 = None)).one()
	session.add(game)

	if game.player1 is None:
		game.player1 = player
	elif game.player2 is None:
		game.player2 = player
	else:
		print("lawl")

	session.add(game)
	session.commit()

	retur

def list():
	games = session.query(Game).filter(_or(player1 = None, player2=None))

	session.add(games)
	print(games)