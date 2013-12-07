import yaml
import orm
from sqlalchemy import or_

def start(session, name, player, scenario="demo"):
	game = orm.Game(name = name, player1 = player, player2 = None, scenario = scenario)

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
